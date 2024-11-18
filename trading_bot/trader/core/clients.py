import json
import os
import urllib.request
from typing import List, Optional

from binance.spot import Spot
from binance.websocket.spot.websocket_api import SpotWebsocketAPIClient
from binance.websocket.spot.websocket_stream import SpotWebsocketStreamClient

from common._logger import logging


class Client(Spot):
    """
    Customising Spot client
    """

    def __init__(
        self, api_key: str = "", api_secret: str = "", test_mode: bool = False, **kwargs
    ):
        if test_mode:
            kwargs["base_url"] = "https://testnet.binance.vision"
        else:
            kwargs["base_url"] = self._server_choice()

        super().__init__(api_key, api_secret, **kwargs)

    def _server_choice(self):
        """
        Server choice

        ! Implement later
        """
        return "https://api2.binance.com"

    def margin_account(self):
        """
        Clear margin_account report. Remove don't using assets
        """
        margin = super().margin_account()
        assets = [
            el
            for el in margin["userAssets"]
            if (
                el["free"] != "0"
                or el["locked"] != "0"
                or el["borrowed"] != "0"
                or el["interest"] != "0"
                or el["netAsset"] != "0"
            )
        ]
        margin["userAssets"] = assets

        return margin

    @staticmethod
    def usdt_all_pairs() -> List[str]:
        """
        Get all pairs with USDT
        """
        response = urllib.request.urlopen(
            "https://api.binance.com/api/v3/exchangeInfo"
        ).read()
        usdt = list(
            map(lambda symbol: symbol["symbol"], json.loads(response)["symbols"])
        )
        return [symbol for symbol in usdt if symbol.endswith("USDT")]


class WSStreamClient(SpotWebsocketStreamClient):
    """
    Customising Stream client
    """

    def __init__(self, message_handler, test_mode: bool = False, **kwargs):
        if test_mode:
            stream_url = "wss://testnet.binance.vision"
        else:
            stream_url = "wss://stream.binance.com:9443"

        super().__init__(
            stream_url,
            on_open=WSStreamClient.on_open,
            on_message=message_handler,
            on_ping=WSStreamClient.on_ping,
            on_pong=WSStreamClient.on_pong,
            on_close=WSStreamClient.on_close,
            is_combined=True,
            **kwargs,
        )

    @staticmethod
    def on_ping(*args):
        logging.info(f"args on_ping: {args}")
        logging.info("received ping from server")

    @staticmethod
    def on_pong(socketManager):
        logging.info("received pong from server")
        # logger.info(kwargs.__repr__())

    @staticmethod
    def on_open(socketManager):
        logging.info("opened connection")

    @staticmethod
    def on_close(socketManager):
        logging.info("Closing connection received")


class WSAPIClient(SpotWebsocketAPIClient):
    def __init__(
        self, key: str = "", secret: str = "", test_mode: bool = False, **kwargs
    ):
        if test_mode:
            streamUrl = "wss://testnet.binance.vision/ws-api/v3"
        else:
            streamUrl = "wss://ws-api.binance.com:443/ws-api/v3"

        super().__init__(
            stream_url=streamUrl,
            api_key=key,
            api_secret=secret,
            on_message=self.message_handler,
            on_open=self.on_open,
            on_close=self.on_close,
            on_error=None,
            on_ping=None,
            on_pong=None,
            timeout=None,
            logger=logging,
        )

    def on_close(self, _):
        logging.info("Do custom stuff when connection is closed")

    def on_open(self, _):
        logging.info("Opened connection")

    def message_handler(self, _, message):
        logging.info(message)


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    # load_dotenv('/home/jb/PycharmProjects/binanceTradeDj/binanceTrade/.env')
    key = os.environ.get("BINANCE_API_KEY")
    secret = os.environ.get("BINANCE_API_SECRET")

    client = Client(key=key, secret=secret)
    logging.info(client.margin_account())
    # logging.error(client.margin_all_pairs())
