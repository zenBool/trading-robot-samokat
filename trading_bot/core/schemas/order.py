from typing import List, Optional
from pydantic import BaseModel, Field

from core.schemas.rate_limit import RateLimit


class Fill(BaseModel):
    price: str
    qty: str
    commission: str
    commissionAsset: str
    tradeId: int


class OrderFull(BaseModel):
    """Full Order Response
    Args:
        symbol (str): The symbol associated with the order.
        orderId (int): The unique identifier of the order.
        orderListId (int): The unique identifier of the associated order list.
        clientOrderId (str): The unique identifier of the order sent by the user.
        transactTime (int): The time of the order creation.
        price (str): The price of the order.
        origQty (str): The original quantity of the order.
        executedQty (str): The quantity of the order that has been filled.
        origQuoteOrderQty (str): The original quote order quantity.
        cummulativeQuoteQty (str): The cumulative quote order quantity filled.
        status (str): The order status (NEW, PARTIALLY_FILLED, FILLED, CANCELED, EXPIRED, REJECTED).
        timeInForce (str): The time in force of the order (GTC, IOC, FOK).
        type (str): The order type (LIMIT, MARKET, STOP_LOSS, STOP_LOSS_LIMIT, TAKE_PROFIT, TAKE_PROFIT_LIMIT).
        side (str): The side of the order (BUY, SELL).
        workingTime (int): The time in force of the order in milliseconds.
        fills (List[Fill]): The fills details.
        selfTradePreventionMode (str): The self trade prevention mode (CANCEL_REPLACE, IGNORE, UPDATE_TAKE_PROFIT, UPDATE_TAKE_LOSS).
        icebergQty (str): The iceberg quantity.
        preventedMatchId (int): The prevented match ID.
        preventedQuantity (str): The prevented quantity.
        stopPrice (str): The stop price.
        strategyId (int): The strategy ID.
        strategyType (int): The strategy type. Must be more than 1000000.
        trailingDelta (int): The trailing delta.
        trailingTime (int): The trailing time in milliseconds.
        usedSor (bool): The used stop-or-replace flag.
        workingFloor (str): The working floor.

    """
    symbol: str
    orderId: int
    orderListId: int
    clientOrderId: str
    transactTime: int
    price: str
    origQty: str
    executedQty: str
    origQuoteOrderQty: str
    cummulativeQuoteQty: str
    status: str
    timeInForce: str
    type: str
    side: str
    workingTime: int
    fills: List[Fill]
    selfTradePreventionMode: str

    # Conditional fields
    icebergQty: Optional[str] = None
    preventedMatchId: Optional[int] = None
    preventedQuantity: Optional[str] = None
    stopPrice: Optional[str] = None
    strategyId: Optional[int] = None
    strategyType: Optional[int] = None
    trailingDelta: Optional[int] = None
    trailingTime: Optional[int] = None
    usedSor: Optional[bool] = None
    workingFloor: Optional[str] = None


class OrderWrapper(BaseModel):
    """Order Response Wrapper

    Args:
        id (str): The unique identifier of the order.
        status (int): The order status (1: New, 2: Partially Filled, 3: Filled, 4: Canceled, 5: Expired, 6: Rejected).
        result (FullOrderResponse): The full order details.
        rateLimits (List[RateLimit]): The rate limits for the API requests.

    """
    id: str
    status: int
    result: OrderFull
    rateLimits: List[RateLimit]
