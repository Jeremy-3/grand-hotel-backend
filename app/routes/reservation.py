from uuid import UUID
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.rbac import require_permission
from app.crud.reservation import crud_reservation
from app.schemas.reservation import ReservationCreate, ReservationUpdate, ReservationOut
from app.schemas.response import ResponseModel

router = APIRouter(prefix="/reservations", tags=["Reservations"])


# ------------------------------------------------------------
# READ - all reservations (staff/management)
# ------------------------------------------------------------
@router.get(
    "",
    response_model=ResponseModel[list[ReservationOut]],
    dependencies=[Depends(require_permission("reservations.view_all"))],
)
def get_reservations(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
):
    crud_reservation.expire_pending_reservations(db)
    records, total = crud_reservation.read(
        db,
        page=page,
        limit=limit,
        relationships=["room", "guest"],
    )
    return ResponseModel(data=records, total=total)


# ------------------------------------------------------------
# CREATE
# ------------------------------------------------------------
@router.post(
    "",
    response_model=ResponseModel[ReservationOut],
    dependencies=[Depends(require_permission("reservations.create"))],
)
def create_reservation(
    payload: ReservationCreate,
    payment_method: str = Query(..., description="mpesa / card / cash / bank_transfer"),
    db: Session = Depends(get_db),
):
    reservation = crud_reservation.create_reservation(db, payload, payment_method)
    return ResponseModel(data=reservation, message="Reservation created successfully")


# ------------------------------------------------------------
# READ - guest's reservations (paginated)
# ------------------------------------------------------------
@router.get(
    "/guest/{guest_id}",
    response_model=ResponseModel[list[ReservationOut]],
    dependencies=[Depends(require_permission("reservations.view_own"))],
)
def get_guest_reservations(
    guest_id: int,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    crud_reservation.expire_pending_reservations(db)
    records, total = crud_reservation.get_guest_reservations(db, guest_id, page, limit)
    return ResponseModel(data=records, total=total)


# ------------------------------------------------------------
# READ - single
# ------------------------------------------------------------
@router.get(
    "/{uid}",
    response_model=ResponseModel[ReservationOut],
    dependencies=[Depends(require_permission("reservations.view_all"))],
)
def get_reservation(
    uid: UUID,
    db: Session = Depends(get_db),
):
    reservation = crud_reservation.get_reservation(db, uid)
    return ResponseModel(data=reservation)


# ------------------------------------------------------------
# UPDATE
# ------------------------------------------------------------
@router.patch(
    "/{uid}",
    response_model=ResponseModel[ReservationOut],
    dependencies=[Depends(require_permission("reservations.edit"))],
)
def update_reservation(
    uid: UUID,
    payload: ReservationUpdate,
    db: Session = Depends(get_db),
):
    reservation = crud_reservation.update_reservation(db, uid, payload)
    return ResponseModel(data=reservation, message="Reservation updated successfully")


# ------------------------------------------------------------
# STATUS LIFECYCLE
# ------------------------------------------------------------
@router.post(
    "/{uid}/confirm",
    response_model=ResponseModel[ReservationOut],
    dependencies=[Depends(require_permission("reservations.confirm"))],
)
def confirm_reservation(
    uid: UUID,
    db: Session = Depends(get_db),
):
    reservation = crud_reservation.confirm_reservation(db, uid)
    return ResponseModel(data=reservation, message="Reservation confirmed")


@router.post(
    "/{uid}/check-in",
    response_model=ResponseModel[ReservationOut],
    dependencies=[Depends(require_permission("reservations.check_in"))],
)
def check_in_reservation(
    uid: UUID,
    db: Session = Depends(get_db),
):
    reservation = crud_reservation.check_in(db, uid)
    return ResponseModel(data=reservation, message="Guest checked in")


@router.post(
    "/{uid}/check-out",
    response_model=ResponseModel[ReservationOut],
    dependencies=[Depends(require_permission("reservations.check_out"))],
)
def check_out_reservation(
    uid: UUID,
    db: Session = Depends(get_db),
):
    reservation = crud_reservation.check_out(db, uid)
    return ResponseModel(data=reservation, message="Guest checked out")


@router.post(
    "/{uid}/cancel",
    response_model=ResponseModel[ReservationOut],
    dependencies=[Depends(require_permission("reservations.cancel"))],
)
def cancel_reservation(
    uid: UUID,
    db: Session = Depends(get_db),
):
    reservation = crud_reservation.cancel_reservation(db, uid)
    return ResponseModel(data=reservation, message="Reservation cancelled")