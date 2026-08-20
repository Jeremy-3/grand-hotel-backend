from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.session import get_db
from app.dependencies.rbac import require_permission
from app.schemas.room_type import RoomTypeCreate, RoomTypeOut, RoomTypeUpdate
from app.crud.room_type import crud_room_type
from app.schemas.response import ResponseModel

router = APIRouter(prefix="/room-types", tags=["Room Types"])


@router.post(
    "",
    response_model=ResponseModel[RoomTypeOut],
    dependencies=[Depends(require_permission("room_types.create"))],
)
def create_room_type(payload: RoomTypeCreate, db: Session = Depends(get_db)):
    room_type = crud_room_type.create_room_type(db, payload)
    return ResponseModel(data=room_type, message="Room type created successfully")


@router.get(
    "",
    response_model=ResponseModel[list[RoomTypeOut]],
    dependencies=[Depends(require_permission("room_types.view"))],
)
def get_room_types(db: Session = Depends(get_db)):
    records, total = crud_room_type.read(db)
    return ResponseModel(
        data=records, total=total, message="Room types retrieved successfully"
    )


@router.get(
    "/{uid}",
    response_model=ResponseModel[RoomTypeOut],
    dependencies=[Depends(require_permission("room_types.view"))],
)
def get_room_type(uid: UUID, db: Session = Depends(get_db)):
    room_type = crud_room_type.get_record_by_field(db, "uid", uid)

    if not room_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Room type not found"
        )

    return ResponseModel(data=room_type, message="Room type retrieved successfully")


@router.put(
    "/{uid}",
    response_model=ResponseModel[RoomTypeOut],
    dependencies=[Depends(require_permission("room_types.edit"))],
)
def update_room_type(uid: UUID, payload: RoomTypeUpdate, db: Session = Depends(get_db)):
    room_type = crud_room_type.update_room_type(db, uid, payload)

    return ResponseModel(data=room_type, message="Room type updated successfully")
