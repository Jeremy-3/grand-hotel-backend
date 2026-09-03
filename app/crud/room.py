from app.models.rooms import Rooms
from app.schemas.room import RoomCreate, RoomUpdate
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.crud.base import CRUDBase
from uuid import UUID


MODEL = Rooms

class CRUDRoom(CRUDBase[MODEL, RoomCreate]):
    """CRUD operations for Room model"""
    def create_room(self, db:Session, record_create:RoomCreate):
        existing_record = self.get_record_by_field(db, "room_number", record_create.room_number)
        if existing_record:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Room number already exists",
            )
        
        return self.create(db, record_create)
    
    def update_room(self, db:Session, uid:UUID, record_in:RoomUpdate):
        record = self.get_record_by_field(db, "uid", uid)
        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Room not found",
            )
        if record_in.room_number and record_in.room_number != record.room_number:
            existing_record = self.get_record_by_field(db, "room_number", record_in.room_number)
            if existing_record:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Room number already exists",
                )

        return self.update(db, record, record_in)

    # def soft_delete_room(self, db:Session, uid:UUID):
    #     record = self.get_record_by_field(db, "uid", uid)
    #     if not record:
    #         raise HTTPException(
    #             status_code=status.HTTP_404_NOT_FOUND,
    #             detail="Room not found",
    #         )
        
    #     db.delete(record)
    #     db.commit()

crud_room = CRUDRoom(MODEL)