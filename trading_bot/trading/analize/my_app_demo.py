#%%
import time

from binance.error import ClientError
from binance.websocket.spot.websocket_api import SpotWebsocketAPIClient
from binance.websocket.spot.websocket_stream import SpotWebsocketStreamClient
from binance.spot import Spot as SpotAPIClient

from common.logger import logger
from core.schemas.order import OrderFull
from trading.analize.utils.prepare_env import get_api_key
from trading.core.account import Account

# test = False
test = True

if test:
    _api_stream_url = "wss://ws-api.testnet.binance.vision/ws-api/v3"
    _stream_url = "wss://stream.testnet.binance.vision"
    _base_url = "https://testnet.binance.vision"
else:
    _api_stream_url = "wss://ws-api.binance.com/ws-api/v3"
    _stream_url = "wss://stream.binance.com:9443"
    _base_url = "https://api.binance.com"

api_key, api_secret = get_api_key(test=test)
symbol = "BNBUSDT"


def my_logger(msg, note=None):
    s = "-" * 30
    if note is not None:
        s = s + note + s
    logger.info(s)
    logger.info(msg)
    logger.info(s)

#%%
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

# You can subscribe to the user data stream from websocket stream, it will broadcast all the events
# related to your account, including order updates, balance updates, etc.
# subscribe User Data stream` 
listenKey = spot_api_client.new_listen_key().get("listenKey")
ws_stream_client.user_data(listen_key=listenKey)

#%%
# Получение балансов
account_state = spot_api_client.account(recvWindow=50000)
account = Account(**account_state)
my_logger(account, 'account')

# balances = [asset for asset in account_state['balances'] if (float(asset['free']) != 0 or float(asset['locked']) != 0)]
balances = [asset for asset in account_state['balances'] if asset['asset'] == symbol.removesuffix('USDT') or asset['asset'] == 'USDT']
my_logger(balances, 'balances')
time.sleep(3)

isOrders = spot_api_client.get_open_orders(symbol=symbol)
my_logger(isOrders, 'isOrders')

#%%
# Удаление всех отложенных ордеров
cancel_orders = True
if cancel_orders and isOrders:
    answer = spot_api_client.cancel_open_orders(symbol, recvWindow=20000)
    my_logger(answer, 'answer on cancel_orders')
    isOrders = spot_api_client.get_open_orders(symbol=symbol)
    my_logger(isOrders, 'DELETE all open orders')

#%%
params_limit = {
    "symbol": symbol,
    "side": "SELL",
    "type": "LIMIT",
    "quantity": 1,
    "timeInForce": "GTC",
    "price": 880,
    "strategyType": 1000001,
}

params_market = {
    "symbol": symbol,
    "side": "SELL",
    "quantity": 17.804,
    # "quoteOrderQty": 12000,
    "type": "MARKET",
    "strategyType": 1000001,
}

params = params_limit


#%%
logger.info("vvvvvvvvvvvvvvv MARKET order 'insufficient balance' vvvvvvvvvvvvvvv")
answer = {}
try:
    answer = spot_api_client.new_order(**params)
    # ws_api_client.new_order(**params_limit)

except ClientError as error:
    logger.error(
        "{} {} error. Status: {}; error code: {}; error message: {}".format(
            params["side"],
            params["type"],
            error.status_code,
            error.error_code,
            error.error_message,
        )
    )
    error_code = error.error_code
else:
    error_code = ''
    new_order = OrderFull(**answer)
    my_logger(new_order, 'LIMIT new_order')

logger.info(f"^^^^^^^^^^^^^^^ {error_code} MARKET order 'insufficient balance' ^^^^^^^^^^^^^^^")

#%%
ws_stream_client.mini_ticker(symbol=symbol)

#%%
ws_stream_client.mini_ticker(symbol=symbol, action="UNSUBSCRIBE")

#%%
# You can create a new order from websocket api
logger.info("vvvvvvvvvvvvvvv ws LIMIT order vvvvvvvvvvvvvvv")
ws_api_client.new_order(**params_limit)
logger.info("^^^^^^^^^^^^^^^ ws LIMIT order ^^^^^^^^^^^^^^^")
time.sleep(15)

#%%
logger.info("vvvvvvvvvvvvvvv ws MARKET order vvvvvvvvvvvvvvv")
ws_api_client.new_order(**params_market)
logger.info("^^^^^^^^^^^^^^^ ws MARKET order ^^^^^^^^^^^^^^^")
time.sleep(15)

#%%
# Limit order
answer = spot_api_client.new_order(
    symbol=symbol,
    side="SELL",
    type="LIMIT",
    timeInForce="GTC",
    quantity=0.01,
    # quoteOrderQty=11,
    price=780,
)

new_order = OrderFull(**answer)
my_logger(new_order, 'LIMIT new_order')
time.sleep(10)

#%%
# Market order
answer = spot_api_client.new_order(
    symbol=symbol,
    side="BUY",
    type="MARKET",
    # quantity=0.01,
    quoteOrderQty=300,
)

new_order = OrderFull(**answer)
my_logger(new_order, 'MARKET new_order')
time.sleep(10)

#%%
logger.info("closing ws connection")
ws_api_client.stop()
ws_stream_client.stop()
