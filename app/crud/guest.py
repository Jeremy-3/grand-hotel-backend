from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.guests import Guests
from app.models.users import Users
from app.core.constants import ROLE_GUEST_ID
from app.schemas.guest import GuestCreate, GuestUpdate

MODEL = Guests


class CRUDGuest(CRUDBase[MODEL, GuestCreate]):
    """CRUD for guest profiles"""

    def create_guest_profile(self, db: Session, record_create: GuestCreate) -> Guests:
        user = db.query(Users).filter(Users.id == record_create.user_id).first()
        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")

        if user.role_id != ROLE_GUEST_ID:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "User is not a guest")

        existing = self.get_record_by_field(db, "user_id", record_create.user_id)
        if existing:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Guest profile already exists for this user")

        return self.create(db, record_create)

    def update_guest(self, db: Session, uid: UUID, record_in: GuestUpdate) -> Guests:
        guest = self.get_record_by_field(db, "uid", uid)
        if not guest:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Guest not found")

        return self.update(db, guest, record_in)

    def get_guest_by_user_id(self, db: Session, user_id: int):
        return self.get_record_by_field(db, "user_id", user_id)

    def deactivate_guest(self, db: Session, uid: UUID) -> Guests:
        guest = self.get_record_by_field(db, "uid", uid)
        if not guest:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Guest not found")
        guest.status = "inactive"
        db.commit()
        db.refresh(guest)
        return guest

    def activate_guest(self, db: Session, uid: UUID) -> Guests:
        guest = self.get_record_by_field(db, "uid", uid)
        if not guest:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Guest not found")
        guest.status = "active"
        db.commit()
        db.refresh(guest)
        return guest


crud_guest = CRUDGuest(MODEL)