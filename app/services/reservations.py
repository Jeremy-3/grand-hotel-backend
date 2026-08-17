from datetime import datetime, timezone
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.reservations import Reservations
from app.models.rooms import Rooms
from app.models.room_types import RoomTypes
from app.models.payments import Payments


def create_reservation(
    db: Session,
    guest_id: int,
    room_id: int,
    check_in_date: datetime,
    check_out_date: datetime,
    payment_method: str,
):
    # ---------------------------------------------------------
    # 1. Validate dates
    # ---------------------------------------------------------
    if check_out_date <= check_in_date:
        raise HTTPException(
            status_code=400, detail="Check-out date must be after check-in date."
        )

    # ---------------------------------------------------------
    # 2. Get the room
    # ---------------------------------------------------------
    room = db.query(Rooms).filter(Rooms.id == room_id).first()

    if not room:
        raise HTTPException(status_code=404, detail="Room not found.")

    # ---------------------------------------------------------
    # 3. Get the room type
    # ---------------------------------------------------------
    room_type = db.query(RoomTypes).filter(RoomTypes.id == room.room_type_id).first()

    if not room_type:
        raise HTTPException(status_code=404, detail="Room type not found.")

    # ---------------------------------------------------------
    # 4. Check whether the room is available
    # ---------------------------------------------------------
    if not room.availability:
        raise HTTPException(status_code=400, detail="Room is currently unavailable.")

    # ---------------------------------------------------------
    # 5. Check for overlapping reservations
    # ---------------------------------------------------------
    conflicting_reservation = (
        db.query(Reservations)
        .filter(
            Reservations.room_id == room_id,
            Reservations.status.in_(["pending", "confirmed", "checked_in"]),
            Reservations.check_in_date < check_out_date,
            Reservations.check_out_date > check_in_date,
        )
        .first()
    )

    if conflicting_reservation:
        raise HTTPException(
            status_code=409, detail="Room is already reserved for the selected dates."
        )

    # ---------------------------------------------------------
    # 6. Calculate the deposit
    # ---------------------------------------------------------
    deposit_amount = room_type.price_per_night * room_type.deposit_percentage / 100

    # ---------------------------------------------------------
    # 7. Create the reservation
    #
    # We store the price and deposit information here as a
    # snapshot so future changes to RoomTypes do not affect
    # existing reservations.
    # ---------------------------------------------------------
    reservation = Reservations(
        guest_id=guest_id,
        room_id=room_id,
        check_in_date=check_in_date,
        check_out_date=check_out_date,
        status="pending",
        room_price_per_night=room_type.price_per_night,
        deposit_percentage=room_type.deposit_percentage,
        deposit_amount=deposit_amount,
    )

    db.add(reservation)
    db.flush()

    # ---------------------------------------------------------
    # 8. Create the deposit payment
    # ---------------------------------------------------------
    payment = Payments(
        reservation_id=reservation.id,
        amount=deposit_amount,
        payment_type="deposit",
        method=payment_method,
        status="pending",
    )

    db.add(payment)

    # ---------------------------------------------------------
    # 9. Save everything
    # ---------------------------------------------------------
    db.commit()

    # Refresh both objects so the generated IDs/UUIDs are
    # available immediately.
    db.refresh(reservation)
    db.refresh(payment)

    return reservation
