from datetime import datetime
from pydantic import BaseModel, field_validator
from typing import Optional, Union
from uuid import UUID
from app.schemas.constants import ROOM_TYPES


class RoomTypeBase(BaseModel):
    name: str
    description: str
    price_per_night: int
    amenities: str
    deposit_percentage: int

    @field_validator("name")
    def validate_room_type_name(cls, v: str) -> str:
        if v not in ROOM_TYPES:
            raise ValueError(f"Room type Must be one of {ROOM_TYPES}")
        return v


class RoomTypeCreate(RoomTypeBase):
    pass


class RoomTypeUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price_per_night: Optional[int] = None
    amenities: Optional[str] = None
    deposit_percentage: Optional[int] = None

    @field_validator("name")
    def validate_room_type_name(cls, v: str) -> str:
        if v is not None and v not in ROOM_TYPES:
            raise ValueError(f"Room type Must be one of {ROOM_TYPES}")
        return v


class RoomTypeOut(RoomTypeBase):
    id: int
    uid: UUID
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,
    }
