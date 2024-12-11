from fastapi import APIRouter, Depends

from core.dependencies import get_broker
from trading.core.broker import Broker

router = APIRouter(tags=["Trade"])


@router.post("/buy")
def buy(
        symbol: str,
        quantity: float = 0,
        quoteOrderQty: float = 0,
        broker: Broker = Depends(get_broker),
):
    return broker.trader.buy_market(symbol, quantity, quoteOrderQty)


@router.post("/sell")
def sell(
        symbol: str,
        quantity: float = 0,
        quoteOrderQty: float = 0,
        broker: Broker = Depends(get_broker),
):
    return broker.trader.sell_market(symbol, quantity, quoteOrderQty)


@router.post("/buy_limit")
def buy_limit(
        symbol: str,
        price: float,
        quantity: float = 0,
        quoteOrderQty: float = 0,
        broker: Broker = Depends(get_broker),
):
    return broker.trader.buy_limit(symbol, price, quantity, quoteOrderQty)


@router.post("/sell_limit")
def sell_limit(
        symbol: str,
        price: float,
        quantity: float = 0,
        quoteOrderQty: float = 0,
        broker: Broker = Depends(get_broker),
):
    return broker.trader.sell_limit(symbol, price, quantity, quoteOrderQty)


@router.get("/open_orders")
def get_open_orders(broker: Broker = Depends(get_broker)):
    return broker.trader.get_all_open_orders()
