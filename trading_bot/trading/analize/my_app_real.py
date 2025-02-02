#!/usr/bin/env python
#%%
"""
    A simple demo for how to:
    - Create a connection to the websocket api
    - Create a connection to the websocket stream
    - Subscribe to the user data stream from websocket stream
    - Create a new order from websocket api
"""

import time
from binance.websocket.spot.websocket_api import SpotWebsocketAPIClient
from binance.websocket.spot.websocket_stream import SpotWebsocketStreamClient
from binance.spot import Spot as SpotAPIClient

from common.logger import logger
from trading.analize.utils.prepare_env import get_api_key
from trading.core.account import Account

# test = False
test = False

if test:
    _api_stream_url = "wss://ws-api.testnet.binance.vision/ws-api/v3"
    _stream_url = "wss://stream.testnet.binance.vision"
    _base_url = "https://testnet.binance.vision"
else:
    _api_stream_url = "wss://ws-api.binance.com/ws-api/v3"
    _stream_url = "wss://stream.binance.com:9443"
    _base_url = "https://api.binance.com"

api_key, api_secret = get_api_key(test=test)


def on_close(_):
    logger.info("Do custom stuff when connection is closed")


def websocket_api_message_handler(_, message):
    logger.info("message from websocket API")
    logger.info(message)


def websocket_stream_message_handler(_, message):
    logger.info("message from websocket stream")
    logger.info(message)


# make a connection to the websocket api
ws_api_client = SpotWebsocketAPIClient(
    stream_url=_api_stream_url,
    api_key=api_key,
    api_secret=api_secret,
    on_message=websocket_api_message_handler,
    on_close=on_close,
)

# make a connection to the websocket stream
ws_stream_client = SpotWebsocketStreamClient(
    stream_url=_stream_url,
    on_message=websocket_stream_message_handler,
)

# spot api client to call all restful api endpoints
spot_api_client = SpotAPIClient(api_key, api_secret, base_url=_base_url)


s_v = "v"*30
s_A = "^"*30
account_state = spot_api_client.account(recvWindow=50000)
account = Account(**account_state)
logger.info("Account state: {}".format(s_A))
balances = [asset for asset in account_state['balances'] if (float(asset['free']) != 0 or float(asset['locked']) != 0)]
logger.info(balances)
logger.info("Balances {}".format(s_A))
time.sleep(1)
full_balance = spot_api_client.balance()
logger.info("full_balance".format(s_v))
logger.info(full_balance)

#%%
# You can subscribe to the user data stream from websocket stream, it will broadcast all the events
# related to your account, including order updates, balance updates, etc.
# response = spot_api_client.new_listen_key()
# ws_stream_client.user_data(listen_key=response["listenKey"])


# You can create a new order from websocket api
# ws_api_client.new_order(
#     symbol="BNBUSDT",
#     side="SELL",
#     type="LIMIT",
#     timeInForce="GTC",
#     quantity=0.02,
#     # quoteOrderQty=11,
#     price=800,
#     newOrderRespType="RESULT",
# )

time.sleep(10)

logger.info("closing ws connection")
ws_api_client.stop()
ws_stream_client.stop()
