from typing import Any

from binance.error import ClientError

from common.logger import logger

from trading.core.clients import Client


class Trader(Client):
    """Parameters for order
    Args:
        symbol (str)
        side (str)
        type (str)
    Keyword Args:
        timeInForce (str, optional) Supported values:
                GTC - Good Til Canceled
                        An order will be on the book unless the order is canceled.
                FOK - Fill or Kill
                        An order will expire if the full order cannot be filled upon execution.
                IOC - Immediate Or Cancel
                        An order will try to fill the order as much as it can before the order expires.
        quantity (float, optional)
        quoteOrderQty (float, optional)
        price (float, optional)
        newClientOrderId (str, optional): A unique id among open orders. Automatically generated if not sent.
        strategyId (int, optional)
        strategyType (int, optional): The value cannot be less than 1000000.
        stopPrice (float, optional): Used with STOP_LOSS, STOP_LOSS_LIMIT, TAKE_PROFIT, and TAKE_PROFIT_LIMIT orders.
        icebergQty (float, optional): Used with LIMIT, STOP_LOSS_LIMIT, and TAKE_PROFIT_LIMIT to create an iceberg order
        newOrderRespType (str, optional): Set the response JSON. ACK, RESULT, or FULL;
                MARKET and LIMIT order types default to FULL, all other orders default to ACK.
        recvWindow (int, optional): The value cannot be greater than 60000
    """

    def __init__(self, cfg: Any, **kwargs):
        super().__init__(
            api_key=cfg.BINANCE_API_KEY,
            api_secret=cfg.BINANCE_API_SECRET,
            **kwargs,
        )
        self._logger = logger

    def buy_limit(self, symbol: str, price: float, quantity: float = 0,  quoteOrderQty: float = 0):
        side = "BUY"

        return self._new_limit_order(symbol, side, price, quantity, quoteOrderQty)

    def sell_limit(self, symbol: str, price: float, quantity: float = 0,  quoteOrderQty: float = 0):
        side = "SELL"

        return self._new_limit_order(symbol, side, price, quantity, quoteOrderQty)

    def buy_market(
        self,
        symbol: str,
        quantity: float = 0,
        quoteOrderQty: float = 0,
    ):
        side = "BUY"

        return self._new_market_order(symbol, side, quantity, quoteOrderQty)

    def sell_market(
        self,
        symbol: str,
        quantity: float = 0,
        quoteOrderQty: float = 0,
    ):
        side = "SELL"

        return self._new_market_order(symbol, side, quantity, quoteOrderQty)

    def cancel_orders_by_symbol(self, symbol: str):
        try:
            self.cancel_open_orders(symbol)
        except Exception:
            self._logger.error("===Failed to cancel orders.===")

    def open(self):
        pass

    def close(self):
        pass

    def _get_all_open_orders(self):
        try:
            return self.get_open_orders()
        except ClientError as error:
            self._logger.error(
                "My Block ERROR. status: {}; error code: {}; error message: {}".format(
                    error.status_code, error.error_code, error.error_message
                )
            )

        return []

    def _new_limit_order(self, symbol: str, side: str, price: float, quantity: float = 0, quoteOrderQty: float = 0):
        if quantity == quoteOrderQty == 0:
            return -1

        if quantity == 0:
            quantity = quoteOrderQty / price

        params = {
            "symbol": symbol,
            "quantity": quantity,
            "price": price,
            "side": side,
            "type": "LIMIT",
            "timeInForce": "GTC",
        }

        return self._new_order(**params)

    def _new_market_order(self, symbol: str, side: str, quantity: float = 0, quoteOrderQty: float = 0):
        params = {
            "symbol": symbol,
            "side": side,
            "type": "MARKET",
        }
        if not quantity:
            if quoteOrderQty:
                params.update({"quoteOrderQty": quoteOrderQty})
        else:
            params.update({"quantity": quantity})

        return self._new_order(params)

    def _new_order(self, params):
        # params = {
        #     "symbol": symbol,
        #     "side": "BUY",
        #     "type": order_type,
        #     "timeInForce": "GTC",
        #     "quantity": quantity,
        #     "price": price,
        # }

        try:
            response = self.new_order(**params)
            self._logger.info(response)
            return response
        except ClientError as error:
            self._logger.error(
                "{} {} error. Status: {}; error code: {}; error message: {}".format(
                    params["side"],
                    params["type"],
                    error.status_code,
                    error.error_code,
                    error.error_message,
                )
            )

        return -1
