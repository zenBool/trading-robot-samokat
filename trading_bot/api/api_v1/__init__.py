from fastapi import APIRouter

from core.config import settings

from .users import router as users_router
from .account import router as account_router
from .trade import router as trade_router

router = APIRouter()  # "/v1"

router.include_router(
    users_router,
    prefix=settings.api.v1.users,
)


router.include_router(
    account_router,
    prefix=settings.api.v1.account,
)


router.include_router(
    trade_router,
    prefix=settings.api.v1.account,
)
