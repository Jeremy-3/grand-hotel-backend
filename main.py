from fastapi import FastAPI,APIRouter,Request,Depends,Response
from fastapi.middleware.cors import CORSMiddleware
from app.handlers import exception_handlers
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.exc import SQLAlchemyError

from app.routes import (
    auth,guest,manager,payment,
    permissions,reservation,role_permission,
    roles,room_type,
    room, user,
)

app = FastAPI(
    title="Grand Hotel API",
    description="Backend API for Grand Hotel — reservations, guests, rooms, and payments.",
    version="0.2.0",
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten this to your actual frontend origin(s) before production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register exception handlers
app.add_exception_handler(StarletteHTTPException, exception_handlers.http_exception_handler)
app.add_exception_handler(RequestValidationError, exception_handlers.validation_exception_handler)
app.add_exception_handler(Exception, exception_handlers.generic_exception_handler)
app.add_exception_handler(SQLAlchemyError, exception_handlers.sqlalchemy_exception_handler)




@app.get("/")
def root():
    return {"message":"⚙️  Starting up Grand Hotel API...",
             "version": "0.2.0",
             "status": "running",
             "endpoint": "/docs"
            }
    
    
# Include all routers
api_router = APIRouter(prefix="/api")

api_router.include_router(auth.router)
api_router.include_router(guest.router)
api_router.include_router(manager.router)
api_router.include_router(payment.router)
api_router.include_router(permissions.router)
api_router.include_router(reservation.router)
api_router.include_router(role_permission.router)
api_router.include_router(roles.router)
api_router.include_router(user.router)
api_router.include_router(room.router)
api_router.include_router(room_type.router)



app.include_router(api_router) # include main router in the app