from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, TIMESTAMP, Numeric, ForeignKey, text
from sqlalchemy.orm import relationship
from app.db.base import Base
from sqlalchemy.dialects.postgresql import UUID


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    uid = Column(
        UUID(as_uuid=True),
        unique=True,
        nullable=False,
        index=True,
        server_default=text("gen_random_uuid()"),
    )

    reservation_id = Column(
        Integer, ForeignKey("reservations.id", ondelete="CASCADE"), nullable=False
    )

    amount = Column(Numeric(10, 2), nullable=False)

    payment_type = Column(String, nullable=False)
    # deposit / balance / full_payment / refund

    payment_method = Column(String, nullable=False)
    # mpesa / card / cash / bank_transfer
    
    payment_status = Column(String, nullable=False, default="pending")
        # pending / paid / failed / cancelled / refunded

    phone = Column(String(20), nullable=True)


    checkout_request_id = Column(String(255), unique=True, nullable=True)

    mpesa_receipt = Column(String(255), unique=True, nullable=True)

    tx_ref = Column(String(255), unique=True, nullable=True)

    flw_tx_id = Column(String(100), nullable=True)

    paid_at = Column(TIMESTAMP(timezone=True), nullable=True)

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

    # relationships
    reservation = relationship("Reservations", back_populates="payments")
