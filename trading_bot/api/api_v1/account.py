from fastapi import APIRouter, Depends

from core.dependencies import get_broker
from trading.core.broker import Broker

router = APIRouter(tags=["Account"])


@router.get("/acc")
def account_overview(broker: Broker = Depends(get_broker)):
    account = broker.account()
    test_mode = broker.config.TEST_MODE
    return account


@router.get("/open_orders")
def all_open_orders(broker: Broker = Depends(get_broker)):
    orders = broker.trader.get_all_open_orders()
    return orders
