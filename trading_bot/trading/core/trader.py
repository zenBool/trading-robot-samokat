from typing import Any

from binance.error import ClientError, ServerError

from common.logger import logger
from core.schemas.account import AccountSchema
from trading.core.account import Account

from trading.core.clients import Client, WSAPIClient, WSStreamClient


class Trader:
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
        self._logger = logger
        self.listenKey: str | None = None
        self.account: AccountSchema | None = None
        self.strategyType: int | None = None

        if not cfg.TEST_MODE:
            key = cfg.BINANCE_API_KEY
            secret = cfg.BINANCE_API_SECRET
        else:
            key = cfg.BINANCE_TESTNET_API_KEY
            secret = cfg.BINANCE_TESTNET_API_SECRET

        self.client = Client(
            api_key=key,
            api_secret=secret,
            test_mode=cfg.TEST_MODE,
            **kwargs,
        )
        response = self.client.new_listen_key()
        self.listenKey = response["listenKey"]

        self.ws_client = WSStreamClient(
            message_handler=self._ws_stream_message_handler,
            test_mode=cfg.TEST_MODE,
            **kwargs,
        )

        self._get_account()

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
        try:
            response = self._new_market_order(symbol, side, quantity, quoteOrderQty)
        except ClientError as error:
            logger.error(error)
        except ServerError as error:
            logger.error(error)

        return

    def sell_market(
        self,
        symbol: str,
        quantity: float = 0,
        quoteOrderQty: float = 0,
    ):
        side = "SELL"

        return self._new_market_order(symbol, side, quantity, quoteOrderQty)

    def cancel_all_orders(self):
        pass

    def cancel_orders_by_symbol(self, symbol: str):
        try:
            self.client.cancel_open_orders(symbol)
        except Exception:
            self._logger.error("===Failed to cancel orders.===")

    def get_all_open_orders(self):
        return self._get_all_open_orders()

    def close(self):
        pass

    def set_strategyType(self, strategyId: int):
        if strategyId < 1000000:
            raise ValueError("strategyId must be greater than to 1000000.")
        self.strategyType = 1000000

    def _get_account(self):
        account_data = self.client.account(recvWindow=5000, omitZeroBalances='true')
        self.account = Account(**account_data)

    def _get_all_open_orders(self):
        try:
            return self.client.get_open_orders()
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
            "symbol": symbol.upper(),
            "quantity": quantity,
            "price": price,
            "side": side,
            "type": "LIMIT",
            "timeInForce": "GTC",
            "strategyType": self.strategyType,
        }

        return self._new_order(**params)

    def _new_market_order(self, symbol: str, side: str, quantity: float = 0, quoteOrderQty: float = 0):
        params = {
            "symbol": symbol.upper(),
            "side": side,
            "type": "MARKET",
            "strategyType": self.strategyType,
        }
        if not quantity:
            if quoteOrderQty:
                params.update({"quoteOrderQty": quoteOrderQty})
        else:
            params.update({"quantity": quantity})

        return self._new_order(**params)

    def _new_order(self, **params: dict) -> Any:
        try:
            response = self.client.new_order(**params)
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
            return -1, error.error_code, error.error_message
        except ServerError as error:
            self._logger.error("Server error: " + error.status_code + error.message)
            return -1, error.status_code,  error.message

        self._logger.debug("raw response:" + response)
        return response

    def _ws_stream_message_handler(self, message):
        # Implement the message handling logic here
        pass
