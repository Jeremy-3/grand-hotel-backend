from app.models.room_types import RoomTypes
from app.schemas.room_type import RoomTypeCreate, RoomTypeUpdate
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.crud.base import CRUDBase
from uuid import UUID

MODEL = RoomTypes


class CRUDRoomType(CRUDBase[MODEL, RoomTypeCreate]):
    """Crud for room types"""

    def create_room_type(self, db: Session, record_create: RoomTypeCreate):
        existing_record = self.get_record_by_field(db, "name", record_create.name)
        if existing_record:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Room type with this name already exists",
            )

        return self.create(db, record_create)

    def update_room_type(self, db: Session, uid: UUID, record_in: RoomTypeUpdate):
        record = self.get_record_by_field(db, "uid", record_in.uid)
        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Room type not found"
            )

        if record_in.name and record_in.name != record.name:
            existing_record = self.get_record_by_field(db, "name", record_in.name)
            if existing_record:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Room Type with this name already exists",
                )
                
        return self.update(db, record, record_in)


crud_room_type = CRUDRoomType(MODEL)
