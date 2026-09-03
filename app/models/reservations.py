from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey,
    DateTime,
    TIMESTAMP,
    func,
    Boolean,
    text,
)
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from app.db.base import Base
from sqlalchemy.dialects.postgresql import UUID


class Reservations(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    uid = Column(
        UUID(as_uuid=True),
        unique=True,
        nullable=False,
        index=True,
        server_default=text("gen_random_uuid()"),
    )

    guest_id = Column(
        Integer, ForeignKey("guests.id", ondelete="CASCADE"), nullable=False
    )

    room_id = Column(
        Integer, ForeignKey("rooms.id", ondelete="RESTRICT"), nullable=False
    )
    
    payment_due_at = Column(DateTime(timezone=True), nullable=False)

    check_in_date = Column(DateTime(timezone=True), nullable=False)

    check_out_date = Column(DateTime(timezone=True), nullable=False)

    status = Column(String, nullable=False, default="pending")

    # Snapshot the agreed price at the time of booking
    room_price_per_night = Column(Integer, nullable=False)

    deposit_percentage = Column(Integer, nullable=False)

    deposit_amount = Column(Integer, nullable=False)
    
    total_amount = Column(Integer, nullable=False)

    created_at = Column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    updated_at = Column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationships

    guest = relationship("Guests", back_populates="reservations")

    room = relationship("Rooms", back_populates="reservations")

    payments = relationship(
        "Payment", back_populates="reservation", cascade="all, delete-orphan"
    )
