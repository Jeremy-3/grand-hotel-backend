from datetime import datetime
from pydantic import BaseModel, field_validator
from typing import Optional, Union
from uuid import UUID
from app.schemas.constants import MANAGER_STATUSES
from app.schemas.user import UserOut


class ManagerBase(BaseModel):
    user_id: int
    status: Optional[str] = "active"

    @field_validator("status")
    def validate_manager_status(cls, v: str) -> str:
        if v not in MANAGER_STATUSES:
            raise ValueError(
                f"Invalid manager status. Must be one of {MANAGER_STATUSES}"
            )
        return v


class ManagerCreate(ManagerBase):
    pass


class ManagerUpdate(BaseModel):
    user_id: Optional[int] = None
    status: Optional[str] = None

    @field_validator("status")
    def validate_manager_status(cls, v: str) -> str:
        if v is not None and v not in MANAGER_STATUSES:
            raise ValueError(
                f"Invalid manager status. Must be one of {MANAGER_STATUSES}"
            )
        return v


class ManagerOut(ManagerBase):
    id: int
    uid: UUID
    user: UserOut = None
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,
    }
