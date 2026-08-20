from uuid import UUID
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.crud.guest import crud_guest
from app.schemas.guest import GuestCreate, GuestUpdate, GuestOut
from app.schemas.response import ResponseModel
from app.dependencies.rbac import require_permission


router = APIRouter(prefix="/guests", tags=["Guests"])

@router.post("", response_model=ResponseModel[GuestOut], dependencies=[Depends(require_permission("guest.create"))])
def create_guest(payload: GuestCreate, db: Session = Depends(get_db)):
    try:
        guest = crud_guest.create_guest_profile(db, payload)
        return ResponseModel(data=guest, message="Guest created successfully")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    
    
@router.put("/{uid}", response_model=ResponseModel[GuestOut], dependencies=[Depends(require_permission("guest.edit"))])
def update_guest(uid: UUID, payload: GuestUpdate, db: Session = Depends(get_db)):
    guest = crud_guest.update_guest(db, uid, payload)
    return ResponseModel(data=guest, message="Guest updated successfully")


@router.get("/{uid}", response_model=ResponseModel[GuestOut], dependencies=[Depends(require_permission("guest_view"))])
def get_guest(uid: UUID, db: Session = Depends(get_db)):
    guest = crud_guest.get_record_by_field(db, "uid", uid)
    if not guest:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Guest not found")
    return ResponseModel(data=guest, message="Guest retrieved successfully")

@router.get("", response_model=ResponseModel[list[GuestOut]], dependencies=[Depends(require_permission("guest.view_all"))])
def get_guests(db: Session = Depends(get_db)):
    guests = crud_guest.read(db)
    return ResponseModel(data=guests, message="Guests retrieved successfully")


