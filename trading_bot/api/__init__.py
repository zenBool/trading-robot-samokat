from fastapi import APIRouter

from core.config import settings

from .api_v1 import router as router_v1

router = APIRouter()  # "API"

router.include_router(
    router_v1,
    prefix=settings.api.v1.prefix,
)
