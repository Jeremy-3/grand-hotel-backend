from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.reservation import router as reservation_router

app = FastAPI(
    title="Grand Hotel API",
    description="Backend API for Grand Hotel — reservations, guests, rooms, and payments.",
    version="0.1.0",
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten this to your actual frontend origin(s) before production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(reservation_router, prefix="/api")

# As you build out routes/auth.py, routes/user.py, routes/guest.py, routes/room.py,
# routes/manager.py, etc., include them here the same way:
#
# from app.routes.auth import router as auth_router
# app.include_router(auth_router, prefix="/api")


@app.get("/")
def root():
    return {"message": "Grand Hotel API is running"}