from pydantic import BaseModel, field_validator
from typing import Optional, Union
from uuid import UUID
from app.schemas.constants import RESERVATION_STATUSES
from app.schemas.guest import GuestOut
from app.schemas.room import RoomOut
from datetime import datetime


class ReservationBase(BaseModel):
    guest_id: int
    room_id: int
    check_in_date: datetime
    check_out_date: datetime
    payment_due_at: datetime
    status: Optional[str] = "pending"
    room_price_per_night: int
    deposit_percentage: int
    deposit_amount: int
    total_amount: int

    @field_validator("status")
    def validate_reservation_status(cls, v: str) -> str:
        if v not in RESERVATION_STATUSES:
            raise ValueError(
                f"Invalid reservation status. Must be one of {RESERVATION_STATUSES}"
            )
        return v


class ReservationCreate(ReservationBase):
    pass


class ReservationUpdate(BaseModel):
    guest_id: Optional[int] = None
    room_id: Optional[int] = None
    check_in_date: Optional[datetime] = None
    check_out_date: Optional[datetime] = None
    payment_due_at: Optional[datetime] = None
    status: Optional[str] = None
    room_price_per_night: Optional[int] = None
    deposit_percentage: Optional[int] = None
    deposit_amount: Optional[int] = None
    total_amount: Optional[int] = None

    @field_validator("status")
    def validate_reservation_status(cls, v: str) -> str:
        if v is not None and v not in RESERVATION_STATUSES:
            raise ValueError(
                f"Invalid reservation status. Must be one of {RESERVATION_STATUSES}"
            )
        return v


class ReservationOut(ReservationBase):
    id: int
    uid: UUID
    guest: GuestOut = None
    room: RoomOut = None
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,
    }
