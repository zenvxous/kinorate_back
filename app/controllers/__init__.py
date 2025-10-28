from fastapi import APIRouter

from app.controllers.movies import router as movies_router
from app.controllers.recentions import router as recentions_router
from app.controllers.tmdb import router as tmdb_router
from app.controllers.users import router as users_router

main_router = APIRouter()

main_router.include_router(users_router)
main_router.include_router(movies_router)
main_router.include_router(recentions_router)
main_router.include_router(tmdb_router)
