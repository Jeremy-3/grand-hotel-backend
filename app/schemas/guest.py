from pydantic import BaseModel,field_validator
from typing import Optional, Union
from uuid import UUID
from app.schemas.user import UserOut
from app.schemas.constants import GUEST_STATUSES

class GuestBase(BaseModel):
    user_id : int
    status : Optional[str] = "active"
    
    @field_validator("status")
    def validate_guest_status(cls, v: str) -> str:
        if v not in GUEST_STATUSES:
            raise ValueError(f"Invalid guest status. Must be one of {GUEST_STATUSES}")
        return v

    
class GuestCreate(GuestBase):
    pass


class GuestUpdate(BaseModel):
    status: Optional[str] = None
    
    @field_validator("status")
    def validate_guest_status(cls, v: str) -> str:
        if v is not None and v not in GUEST_STATUSES:
            raise ValueError(f"Invalid guest status. Must be one of {GUEST_STATUSES}")
        return v
    
    
class GuestOut(GuestBase):
    id: int
    uid: UUID
    user: UserOut = None
    created_at: str
    updated_at: str

    model_config = {
        "from_attributes": True,
    }

    