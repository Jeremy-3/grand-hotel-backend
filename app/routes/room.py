from uuid import UUID
from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.rbac import require_permission
from app.crud.room import crud_room
from app.schemas.room import RoomCreate, RoomOut, RoomUpdate
from app.schemas.response import ResponseModel

router = APIRouter(prefix="/rooms", tags=["Rooms"])


@router.post(
    "",
    response_model=ResponseModel[RoomOut],
    dependencies=[Depends(require_permission("room.create"))],
)
def create_room(payload: RoomCreate, db: Session = Depends(get_db)):
    room = crud_room.create_room(db, payload)

    return ResponseModel(data=room, message="room made successfully")


@router.get(
    "",
    response_model=ResponseModel[list[RoomOut]],
    dependencies=[Depends(require_permission("room.view_all"))],
)
def get_all_rooms(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    room_availability: str | None = Query(None),
):
    filters = (
        [{"field": "room_availability", "value": room_availability}]
        if room_availability
        else None
    )
    rooms, total = crud_room.read(db, page=page, limit=limit, filters=filters)

    return ResponseModel(data=rooms, message="All rooms retrieved", total=total)


@router.put(
    "/{uid}",
    response_model=ResponseModel[RoomUpdate],
    dependencies=[Depends(require_permission("room.update"))],
)
def update_room(payload: RoomUpdate, uid: UUID, db: Session = Depends(get_db)):
    room = crud_room.update_room(db, uid, payload)

    return ResponseModel(data=room, message="Room updated Successfully")


@router.get(
    "/{uid}",
    response_model=ResponseModel[RoomOut],
    dependencies=[Depends(require_permission("room.view_one"))],
)
def get_one_room(uid: UUID, db: Session = Depends(get_db)):
    room = crud_room.get_record_by_field(db, "uid", uid)
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Room not FOund"
        )

    return ResponseModel(data=RoomOut, message="Room retrieved Successfully")
