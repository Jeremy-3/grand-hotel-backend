from datetime import datetime
from pydantic import BaseModel, field_validator
from typing import Optional, Union
from uuid import UUID
from app.schemas.constants import ROOM_AVAILABILITY_STATUSES


class RoomBase(BaseModel):
    room_number: int
    room_type_id: int
    room_availability: Optional[str] = "available"
    image: str


class RoomCreate(RoomBase):
    room_number: int
    room_type_id: int
    room_availability: Optional[str] = "available"
    image: str

    @field_validator("room_availability")
    def validate_room_availability(cls, v: str) -> str:
        if v not in ROOM_AVAILABILITY_STATUSES:
            raise ValueError(
                f"Invalid room availability. Must be one of {ROOM_AVAILABILITY_STATUSES}"
            )
        return v


class RoomUpdate(BaseModel):
    room_number: Optional[int] = None
    room_type_id: Optional[int] = None
    room_availability: Optional[str] = None
    image: Optional[str] = None

    @field_validator("room_availability")
    def validate_room_availability(cls, v: str) -> str:
        if v is not None and v not in ROOM_AVAILABILITY_STATUSES:
            raise ValueError(
                f"Invalid room availability. Must be one of {ROOM_AVAILABILITY_STATUSES}"
            )
        return v


class RoomOut(RoomBase):
    id: int
    uid: UUID
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,
    }
