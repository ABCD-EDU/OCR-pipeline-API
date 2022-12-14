from api.routes_info import route_models
from fastapi import APIRouter

app_router = APIRouter()

app_router.include_router(route_models.router, prefix="/models", tags=["models"])