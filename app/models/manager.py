from sqlalchemy import Column,String,Integer,ForeignKey,DateTime,TIMESTAMP,func,Boolean,text
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from app.db.base import Base
from sqlalchemy.dialects.postgresql import UUID



class Managers(Base):
    __tablename__ = "managers"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    uid = Column(UUID(as_uuid=True), unique=True, nullable=False, server_default=text("gen_random_uuid()"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False) # timezone = True ensures that the column is timezone-aware. # lambda function, ensures that a new timestamp is generated each time a record is created or updated.
    updated_at = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    
    # relationships
    user = relationship("Users", back_populates="manager")