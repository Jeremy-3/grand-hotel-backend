from pydantic import BaseModel, field_validator
from typing import Optional, Union
from uuid import UUID
from app.schemas.constants import PAYMENT_TYPES, PAYMENT_STATUSES, PAYMENT_METHODS
from datetime import datetime


class PaymentBase(BaseModel):
    reservation_id: int
    amount: int
    payment_type: str
    payment_method: str
    payment_status: str = "pending"
    phone: Optional[str] = None

    @field_validator("payment_type")
    def validate_payment_type(cls, v: str) -> str:
        if v not in PAYMENT_TYPES:
            raise ValueError(f"Invalid payment type. Must be one of {PAYMENT_TYPES}")
        return v

    @field_validator("payment_method")
    def validate_payment_method(cls, v: str) -> str:
        if v not in PAYMENT_METHODS:
            raise ValueError(
                f"Invalid payment method. Must be one of {PAYMENT_METHODS}"
            )
        return v

    @field_validator("payment_status")
    def validate_payment_status(cls, v: str) -> str:
        if v not in PAYMENT_STATUSES:
            raise ValueError(
                f"Invalid payment status. Must be one of {PAYMENT_STATUSES}"
            )
        return v


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(BaseModel):
    reservation_id: Optional[int] = None
    amount: Optional[int] = None
    payment_type: Optional[str] = None
    payment_method: Optional[str] = None
    payment_status: Optional[str] = None
    phone: Optional[str] = None

    @field_validator("payment_type")
    def validate_payment_type(cls, v: str) -> str:
        if v is not None and v not in PAYMENT_TYPES:
            raise ValueError(f"Invalid payment type. Must be one of {PAYMENT_TYPES}")
        return v

    @field_validator("payment_method")
    def validate_payment_method(cls, v: str) -> str:
        if v is not None and v not in PAYMENT_METHODS:
            raise ValueError(
                f"Invalid payment method. Must be one of {PAYMENT_METHODS}"
            )
        return v

    @field_validator("payment_status")
    def validate_payment_status(cls, v: str) -> str:
        if v is not None and v not in PAYMENT_STATUSES:
            raise ValueError(
                f"Invalid payment status. Must be one of {PAYMENT_STATUSES}"
            )
        return v


class PaymentOut(BaseModel):
    id: int
    uid: UUID
    amount: int
    payment_type: str
    payment_method: str
    checkout_request_id: Optional[str] = None
    mpesa_receipt: Optional[str] = None
    tx_ref: Optional[str] = None
    payment_status: str
    paid_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,
    }
