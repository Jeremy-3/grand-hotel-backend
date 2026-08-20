from datetime import datetime, timezone
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.crud.reservation import crud_reservation
from app.models.payments import Payment
from app.models.reservations import Reservations
from app.schemas.payments import PaymentCreate, PaymentUpdate

MODEL = Payment


class CRUDPayment(CRUDBase[MODEL, PaymentCreate]):
    """CRUD for payments, plus the confirm/fail/refund lifecycle."""

    # ------------------------------------------------------------
    # create
    # ------------------------------------------------------------
    def create_payment(self, db: Session, record_create: PaymentCreate) -> Payment:
        reservation = (
            db.query(Reservations)
            .filter(Reservations.id == record_create.reservation_id)
            .first()
        )
        if not reservation:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Reservation not found")

        return self.create(db, record_create)

    # ------------------------------------------------------------
    # read
    # ------------------------------------------------------------
    def get_payment(self, db: Session, uid: UUID) -> Payment:
        payment = self.get_record_by_field(db, "uid", uid)
        if not payment:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Payment not found")
        return payment

    def get_reservation_payments(
        self, db: Session, reservation_id: int, page: int = 1, limit: int = 10
    ):
        return self.read(
            db,
            page=page,
            limit=limit,
            filters=[{"field": "reservation_id", "value": reservation_id}],
        )

    # ------------------------------------------------------------
    # update (generic field edits - amount, method, phone, etc.)
    # ------------------------------------------------------------
    def update_payment(
        self, db: Session, uid: UUID, record_in: PaymentUpdate
    ) -> Payment:
        payment = self.get_payment(db, uid)

        if payment.payment_status in ("paid", "refunded"):
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                f"Cannot modify a {payment.payment_status} payment",
            )

        return self.update(db, payment, record_in)

    # ------------------------------------------------------------
    # lifecycle
    # ------------------------------------------------------------
    def confirm_payment(
        self,
        db: Session,
        uid: UUID,
        mpesa_receipt: str | None = None,
        tx_ref: str | None = None,
        checkout_request_id: str | None = None,
        flw_tx_id: str | None = None,
    ) -> Payment:
        payment = self.get_payment(db, uid)

        if payment.payment_status == "paid":
            if payment.payment_type in ("deposit", "full_payment"):
                reservation = (
                    db.query(Reservations)
                    .filter(Reservations.id == payment.reservation_id)
                    .first()
                )
                if reservation and reservation.status == "pending":
                    crud_reservation.confirm_reservation(db, reservation.uid)
            return payment
        if payment.payment_status == "refunded":
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, "Cannot confirm a refunded payment"
            )

        payment.payment_status = "paid"
        payment.paid_at = datetime.now(timezone.utc)

        if mpesa_receipt:
            payment.mpesa_receipt = mpesa_receipt
        if tx_ref:
            payment.tx_ref = tx_ref
        if checkout_request_id:
            payment.checkout_request_id = checkout_request_id
        if flw_tx_id:
            payment.flw_tx_id = flw_tx_id

        db.commit()
        db.refresh(payment)

        # If this was the deposit payment and the reservation is still
        # pending on it, move the reservation to confirmed automatically.
        if payment.payment_type in ("deposit", "full_payment"):
            reservation = (
                db.query(Reservations)
                .filter(Reservations.id == payment.reservation_id)
                .first()
            )
            if reservation and reservation.status == "pending":
                crud_reservation.confirm_reservation(db, reservation.uid)

        db.refresh(payment)
        return payment

    def fail_payment(self, db: Session, uid: UUID) -> Payment:
        payment = self.get_payment(db, uid)

        if payment.payment_status == "paid":
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "Cannot fail a payment already marked as paid",
            )

        payment.payment_status = "failed"
        db.commit()
        db.refresh(payment)
        return payment

    def refund_payment(self, db: Session, uid: UUID) -> Payment:
        payment = self.get_payment(db, uid)

        if payment.payment_status != "paid":
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, "Only paid payments can be refunded"
            )

        payment.payment_status = "refunded"
        db.commit()
        db.refresh(payment)
        return payment


crud_payment = CRUDPayment(MODEL)
