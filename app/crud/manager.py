from app.models.manager import Managers
from app.schemas.manager import ManagerCreate, ManagerUpdate
from app.core.constants import ROLE_MANAGER_ID
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.crud.base import CRUDBase
from uuid import UUID
from app.models.users import Users


MODEL = Managers

class CRUDManager(CRUDBase[MODEL,ManagerCreate]):
    """"Crud to manage managers"""
    
    def create_manager(self, db:Session, record_create:ManagerCreate):
        # ensure user exists first 
        user = db.query(Users).filter(Users.id == record_create.user_id).first()
        if not user:
            raise HTTPException(404, "User not found")
        
        # ensure correct role 
        if user.role_id != ROLE_MANAGER_ID:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is not a manager"
            )
            
        existing = self.get_record_by_field(db, "user_id", record_create.user_id)
        if existing:
            raise HTTPException(400, "User is already a manager")

        return self.create(db, record_create)
    
    
    def update_manager(self, db: Session, uid: UUID, record_in: ManagerUpdate):
        manager = self.get_record_by_field(db, "uid", uid)
        if not manager:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Manager not found"
            )

        return self.update(db, manager, record_in)
    
    
    def get_manager_by_user_id(self, db: Session, user_id: int):
        return self.get_record_by_field(db, "user_id", user_id)
    
    
    def get_available_managers(self, db: Session):
        return (
            db.query(Managers)
            .filter(Managers.status == "active")
            .all()
        )
    
    
    def deactivate_manager(self, db: Session, uid: UUID):
        manager = self.get_record_by_field(db, "uid", uid)
        if not manager:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Manager not found"
            )

        manager.status = "inactive"
        db.commit()
        
        return manager
    
    def activate_manager(self,db:Session, uid:UUID):
        manager = self.get_record_by_field(db, "uid", uid)
        if not manager:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Guest not Found"
            )
        
        manager.status = "active"
        db.commit()
        
        return manager
    


crud_manager = CRUDManager(MODEL)
