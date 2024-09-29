from fastapi import APIRouter

from src.api.v1.endpoints.health import router as health_router
from src.api.v1.endpoints.robot import router as robot_router

api_router = APIRouter()

api_router.include_router(health_router, prefix="/health", tags=["health"])
api_router.include_router(
    robot_router, prefix="/tibber-developer-test/enter-path", tags=["robot"]
)  # prefix="/robot"
