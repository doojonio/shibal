from fastapi import APIRouter

from .users import router as users_router
from .orders import router as orders_router
from .operations import router as operations_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(users_router)
api_router.include_router(orders_router)
api_router.include_router(operations_router)
