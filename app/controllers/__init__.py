from fastapi import APIRouter

from app.controllers.users import router as users_router

main_router = APIRouter()

main_router.include_router(users_router)
