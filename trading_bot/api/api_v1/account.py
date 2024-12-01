from fastapi import APIRouter, Depends

from core.dependencies import get_broker
from trading.core.broker import Broker

router = APIRouter(tags=["Account"])


@router.get("/acc")
def account_overview(broker: Broker = Depends(get_broker)):
    account = broker.account()
    return account
