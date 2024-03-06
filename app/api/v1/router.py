from fastapi import APIRouter

from app.api.v1.health.router import router as health_router
from app.api.v1.users.router import router as user_router
from app.api.v1.posts.router import router as post_router

api_router = APIRouter()

api_router.include_router(health_router, prefix="/health")
api_router.include_router(user_router, prefix="/users")
api_router.include_router(post_router, prefix="/posts")