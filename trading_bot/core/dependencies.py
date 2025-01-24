from trading_bot.trading.core.broker import Broker

_broker_instance = None


def get_broker() -> Broker:
    global _broker_instance
    if _broker_instance is None:
        _broker_instance = Broker()
    return _broker_instance
