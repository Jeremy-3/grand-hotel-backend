from uuid import UUID
from fastapi import HTTPException, Depends, status, APIRouter, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.rbac import require_permission
from app.crud.manager import crud_manager
from app.schemas.manager import ManagerCreate,ManagerUpdate,ManagerOut
from app.schemas.response import ResponseModel

router = APIRouter(prefix="/managers", tags=["Managers"])

@router.post("", response_model=ResponseModel[ManagerCreate], dependencies=[Depends(require_permission("manager.create"))])
def create_manager(
    payload: ManagerCreate,
    db: Session = Depends(get_db),
):
    manager = crud_manager.create_manager(db, payload)
    
    return ResponseModel(data = manager, message="Manager Created Successfully")

@router.get("",response_model=ResponseModel[list[ManagerOut]], dependencies=[Depends(require_permission("manager.view_all"))])
def get_all(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
):
    manager, total = crud_manager.read(db,page=page, limit=limit)
    
    return ResponseModel(data=manager, message="Managers Retrieved successfully", total=total)


@router.put("/{uid}", response_model=ResponseModel[ManagerUpdate], dependencies=[Depends(require_permission("manager.update"))])
def update_manager(
    payload: ManagerUpdate,
    uid: UUID,
    db: Session = Depends(get_db),
):
    manager = crud_manager.update_manager(db, uid, payload)
    
    return ResponseModel(data = manager, message="manager updated successfully")

@router.get("/{uid}",response_model=ResponseModel[ManagerOut], dependencies=[Depends(require_permission("manager.view_one"))])
def get_one(
    uid: UUID,
    db: Session = Depends(get_db)
):
    manager = crud_manager.get_record_by_field(db, "uid" , uid)
    if not manager:
        raise HTTPException(404, detail="Manager not Found")
    
    return ResponseModel(data=manager, message="Manager retrieved successfully")





    