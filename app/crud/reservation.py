from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.reservations import Reservations
from app.models.guests import Guests
from app.models.rooms import Rooms
from app.models.room_types import RoomTypes
from app.models.payments import Payment
from app.schemas.reservation import ReservationCreate, ReservationUpdate
from app.core.constants import PENDING_RESERVATION_TIMEOUT_DAYS

MODEL = Reservations

# statuses that "hold" a room, i.e. count toward an overlap conflict
ACTIVE_STATUSES = ("pending", "confirmed", "checked_in")


class CRUDReservation(CRUDBase[MODEL, ReservationCreate]):
    """CRUD + booking logic for reservations"""

    # ------------------------------------------------------------
    # helpers
    # ------------------------------------------------------------
    def expire_pending_reservations(self, db: Session) -> int:
        now = datetime.now(timezone.utc)
        expired_count = (
            db.query(Reservations)
            .filter(
                Reservations.status == "pending",
                Reservations.payment_due_at <= now,
            )
            .update({Reservations.status: "expired"}, synchronize_session=False)
        )
        if expired_count:
            db.commit()
        return expired_count

    def _validate_date_order(self, check_in: datetime, check_out: datetime) -> None:
        if check_in >= check_out:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, "Check-out must be after check-in"
            )

    def check_room_availability(
        self,
        db: Session,
        room_id: int,
        check_in: datetime,
        check_out: datetime,
        exclude_reservation_id: Optional[int] = None,
    ) -> bool:
        """True if room_id is free for [check_in, check_out)."""
        self.expire_pending_reservations(db)
        query = db.query(Reservations).filter(
            Reservations.room_id == room_id,
            Reservations.status.in_(ACTIVE_STATUSES),
            Reservations.check_in_date < check_out,
            Reservations.check_out_date > check_in,
        )
        if exclude_reservation_id:
            query = query.filter(Reservations.id != exclude_reservation_id)

        return query.first() is None

    # ------------------------------------------------------------
    # create
    # ------------------------------------------------------------
    def create_reservation(
        self,
        db: Session,
        record_create: ReservationCreate,
        payment_method: str,
    ) -> Reservations:
        # Step 1 — guest exists
        guest = db.query(Guests).filter(Guests.id == record_create.guest_id).first()
        if not guest:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Guest not found")

        # Step 2 — room exists and is bookable
        room = db.query(Rooms).filter(Rooms.id == record_create.room_id).first()
        if not room:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Room not found")
        if not room.status or room.room_availability != "available":
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, "Room is not available for booking"
            )

        # Step 3 — dates
        check_in_dt = record_create.check_in_date
        check_out_dt = record_create.check_out_date
        self._validate_date_order(check_in_dt, check_out_dt)

        # Step 4 — overlap check
        if not self.check_room_availability(db, room.id, check_in_dt, check_out_dt):
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "Room is already booked for the selected dates",
            )

        # Step 5 — price snapshot from RoomType, never from the client
        room_type = (
            db.query(RoomTypes).filter(RoomTypes.id == room.room_type_id).first()
        )
        if not room_type:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, "Room has no room type configured"
            )

        nights = (check_out_dt.date() - check_in_dt.date()).days
        deposit_amount = round(
            room_type.price_per_night * nights * room_type.deposit_percentage / 100
        )
        payment_due_at = datetime.now(timezone.utc) + timedelta(
            days=PENDING_RESERVATION_TIMEOUT_DAYS
        )

        db_obj = Reservations(
            guest_id=guest.id,
            room_id=room.id,
            payment_due_at=payment_due_at,
            check_in_date=check_in_dt,
            check_out_date=check_out_dt,
            status="pending",
            room_price_per_night=room_type.price_per_night,
            deposit_percentage=room_type.deposit_percentage,
            deposit_amount=deposit_amount,
            total_amount=room_type.price_per_night * nights,
        )

        try:
            db.add(db_obj)
            db.flush()  # assigns db_obj.id without committing yet

            payment = Payment(
                reservation_id=db_obj.id,
                amount=deposit_amount,
                payment_type="deposit",
                payment_method=payment_method,
                payment_status="pending",
            )
            db.add(payment)

            db.commit()
            db.refresh(db_obj)
            db.refresh(payment)
        except SQLAlchemyError:
            db.rollback()
            raise HTTPException(500, "Failed to create reservation")

        return db_obj

    # ------------------------------------------------------------
    # read
    # ------------------------------------------------------------
    def get_reservation(self, db: Session, uid: UUID) -> Reservations:
        reservation = self.get_record_by_field(db, "uid", uid)
        if not reservation:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Reservation not found")
        return reservation

    def get_guest_reservations(
        self, db: Session, guest_id: int, page: int = 1, limit: int = 10
    ):
        self.expire_pending_reservations(db)
        return self.read(
            db,
            page=page,
            limit=limit,
            filters=[{"field": "guest_id", "value": guest_id}],
            relationships=["room", "guest"],
        )

    # ------------------------------------------------------------
    # update — only pending/confirmed reservations are editable,
    # and any date/room change re-runs the overlap check
    # ------------------------------------------------------------
    def update_reservation(
        self, db: Session, uid: UUID, record_in: ReservationUpdate
    ) -> Reservations:
        reservation = self.get_reservation(db, uid)

        if reservation.status in ("checked_out", "cancelled", "expired"):
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                f"Cannot modify a {reservation.status} reservation",
            )

        needs_recheck = (
            record_in.room_id or record_in.check_in_date or record_in.check_out_date
        )
        if needs_recheck:
            new_room_id = record_in.room_id or reservation.room_id
            new_check_in = record_in.check_in_date or reservation.check_in_date
            new_check_out = record_in.check_out_date or reservation.check_out_date

            self._validate_date_order(new_check_in, new_check_out)

            if not self.check_room_availability(
                db,
                new_room_id,
                new_check_in,
                new_check_out,
                exclude_reservation_id=reservation.id,
            ):
                raise HTTPException(
                    status.HTTP_400_BAD_REQUEST,
                    "Room is already booked for the selected dates",
                )

        return self.update(db, reservation, record_in)

    # ------------------------------------------------------------
    # status lifecycle
    # ------------------------------------------------------------
    def _transition(
        self, db: Session, uid: UUID, allowed_from: tuple, new_status: str
    ) -> Reservations:
        reservation = self.get_reservation(db, uid)
        if reservation.status not in allowed_from:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                f"Cannot move reservation from '{reservation.status}' to '{new_status}'",
            )
        reservation.status = new_status
        db.commit()
        db.refresh(reservation)
        return reservation

    def confirm_reservation(self, db: Session, uid: UUID) -> Reservations:
        return self._transition(db, uid, ("pending",), "confirmed")

    def check_in(self, db: Session, uid: UUID) -> Reservations:
        return self._transition(db, uid, ("confirmed",), "checked_in")

    def check_out(self, db: Session, uid: UUID) -> Reservations:
        return self._transition(db, uid, ("checked_in",), "checked_out")

    def cancel_reservation(self, db: Session, uid: UUID) -> Reservations:
        return self._transition(
            db, uid, ("pending", "confirmed", "checked_in"), "cancelled"
        )

    def expire_reservation(self, db: Session, uid: UUID) -> Reservations:
        return self._transition(db, uid, ("pending",), "expired")


crud_reservation = CRUDReservation(MODEL)
