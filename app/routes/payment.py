from uuid import UUID
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.rbac import require_permission
from app.crud.payment import crud_payment
from app.schemas.payments import PaymentCreate, PaymentUpdate, PaymentOut
from app.schemas.response import ResponseModel

router = APIRouter(prefix="/payments", tags=["Payments"])


# ------------------------------------------------------------
# CREATE
# ------------------------------------------------------------
@router.post("", response_model=ResponseModel[PaymentOut])
def create_payment(
    payload: PaymentCreate,
    db: Session = Depends(get_db),
    _: bool = Depends(require_permission("payments.process")),
):
    payment = crud_payment.create_payment(db, payload)
    return ResponseModel(data=payment, message="Payment record created")


# ------------------------------------------------------------
# READ - single
# ------------------------------------------------------------
@router.get("/{uid}", response_model=ResponseModel[PaymentOut])
def get_payment(
    uid: UUID,
    db: Session = Depends(get_db),
    _: bool = Depends(require_permission("payments.view_details")),
):
    payment = crud_payment.get_payment(db, uid)
    return ResponseModel(data=payment)


# ------------------------------------------------------------
# READ - all payments for a reservation (paginated)
# ------------------------------------------------------------
@router.get("/reservation/{reservation_id}", response_model=ResponseModel[list[PaymentOut]])
def get_reservation_payments(
    reservation_id: int,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    _: bool = Depends(require_permission("payments.view_own")),
):
    records, total = crud_payment.get_reservation_payments(db, reservation_id, page, limit)
    return ResponseModel(data=records, total=total)


# ------------------------------------------------------------
# UPDATE (edit before it's confirmed - e.g. wrong phone/method)
# ------------------------------------------------------------
@router.patch("/{uid}", response_model=ResponseModel[PaymentOut])
def update_payment(
    uid: UUID,
    payload: PaymentUpdate,
    db: Session = Depends(get_db),
    _: bool = Depends(require_permission("payments.process")),
):
    payment = crud_payment.update_payment(db, uid, payload)
    return ResponseModel(data=payment, message="Payment updated")


# ------------------------------------------------------------
# LIFECYCLE
# ------------------------------------------------------------
@router.post("/{uid}/confirm", response_model=ResponseModel[PaymentOut])
def confirm_payment(
    uid: UUID,
    mpesa_receipt: str | None = Query(None),
    tx_ref: str | None = Query(None),
    checkout_request_id: str | None = Query(None),
    flw_tx_id: str | None = Query(None),
    db: Session = Depends(get_db),
    _: bool = Depends(require_permission("payments.verify")),
):
    payment = crud_payment.confirm_payment(
        db,
        uid,
        mpesa_receipt=mpesa_receipt,
        tx_ref=tx_ref,
        checkout_request_id=checkout_request_id,
        flw_tx_id=flw_tx_id,
    )
    return ResponseModel(data=payment, message="Payment confirmed")


@router.post("/{uid}/fail", response_model=ResponseModel[PaymentOut])
def fail_payment(
    uid: UUID,
    db: Session = Depends(get_db),
    _: bool = Depends(require_permission("payments.verify")),
):
    payment = crud_payment.fail_payment(db, uid)
    return ResponseModel(data=payment, message="Payment marked as failed")


@router.post("/{uid}/refund", response_model=ResponseModel[PaymentOut])
def refund_payment(
    uid: UUID,
    db: Session = Depends(get_db),
    _: bool = Depends(require_permission("payments.refund")),
):
    payment = crud_payment.refund_payment(db, uid)
    return ResponseModel(data=payment, message="Payment refunded")


