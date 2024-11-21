import calendar
import configparser
from pathlib import Path
from typing import List, Annotated, Any

from pydantic import BaseModel, AfterValidator

from common.logger import logger
from trading.enums import enums

from trading.core.clients import Client
from trading.core.settings import BASE_DIR, settings

CFG_FL_NAME = "trader.cfg"
LOGGING_SECTION = "Logging"
USER_CFG_SECTION = "binance"
STRATEGY_SECTION = "strategy"

cfg = configparser.ConfigParser()
cfg_file = Path(BASE_DIR, CFG_FL_NAME)
if not Path.is_file(cfg_file):
    raise FileNotFoundError("No configuration file %r found!".format(CFG_FL_NAME))
else:
    cfg.read(cfg_file)


_all_usdt_pairs = Client.usdt_all_pairs()


def get_supported_symbols_list(quote: str) -> List[str]:
    # Get supported coin list from supported_coin_list file
    supported_symbols_list: List[Annotated[str, AfterValidator(check_symbol)]] = []
    path_coin_list = Path(BASE_DIR, "txt/supported_coin_list")
    if Path.is_file(path_coin_list):
        with open(path_coin_list) as rfh:
            for line in rfh:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                supported_symbols_list.append(line.upper() + quote)
            logger.info(f"reading supported_coin_list file: {rfh.name}")
    else:
        supported_symbols_list = [
            "BTCUSDT",
            "ETHUSDT",
            "BNBUSDT",
            "XMRUSDT",
            "VETUSDT",
            "MATICUSDT",
            "ADAUSDT",
        ]

    # supported_symbols_list = enums.SYMBOLS
    supported_symbols_list = enums.SYMBOLS_OTHER[25:]

    return supported_symbols_list


def check_symbol(v: str) -> str:
    assert v in _all_usdt_pairs, f"{v} is invalid SYMBOL name"
    return v


def check_timeframe(v: str) -> str:
    assert v in enums.TIMEFRAMES.keys(), f"{v} is invalid TIMEFRAME name"
    return v


class Config(BaseModel):
    # Get config for binance
    TEST_MODE: bool = cfg.get(USER_CFG_SECTION, "test_mode").lower() == "true"
    # Самая ранняя дата с которой работает приложение в мс
    OLDEST_TIME: int = calendar.timegm((2019, 1, 1, 0, 0, 0)) * 1000

    BINANCE_API_KEY: str = settings.binance.api_key
    BINANCE_API_SECRET: str = settings.binance.api_secret
    BINANCE_TLD: str = settings.binance.tld or "com"

    #############
    # дописать проверку поддержки биржей сформированных символов
    #############
    SYMBOLS_LIST: List[str] = get_supported_symbols_list("USDT")

    FAST: Annotated[str, AfterValidator(check_timeframe)] = cfg.get(
        STRATEGY_SECTION, "fast"
    )
    MIDDLE: Annotated[str, AfterValidator(check_timeframe)] = cfg.get(
        STRATEGY_SECTION, "middle"
    )
    LONG: Annotated[str, AfterValidator(check_timeframe)] = cfg.get(
        STRATEGY_SECTION, "long"
    )
    VLONG: Annotated[str, AfterValidator(check_timeframe)] = cfg.get(
        STRATEGY_SECTION, "vlong"
    )
    TIMEFRAMES_LIST: Any = None

    STRATEGY: str = cfg.get(STRATEGY_SECTION, "name")

    SCOUT_SLEEP_TIME: int = cfg.getint(STRATEGY_SECTION, "scout_sleep_time") or 10

    BASE_COIN: str = cfg.get(STRATEGY_SECTION, "base_coin") or "USDT"

    LIPS: int = cfg.getint(STRATEGY_SECTION, "lips")
    TEETH: int = cfg.getint(STRATEGY_SECTION, "teeth")
    JAW: int = cfg.getint(STRATEGY_SECTION, "jaw")

    LEVEL_UP: int = cfg.getint(STRATEGY_SECTION, "level_up")
    LEVEL_DOWN: int = cfg.getint(STRATEGY_SECTION, "level_down")

    BARS_LIMIT: int = cfg.getint(STRATEGY_SECTION, "bars_limit") or 1000

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        assert (
            enums.TIMEFRAMES[self.FAST]
            < enums.TIMEFRAMES[self.MIDDLE]
            < enums.TIMEFRAMES[self.LONG]
        ), f"Incorrect sequence of timeframes: {self.FAST} < {self.MIDDLE} < {self.LONG}"
        self.TIMEFRAMES_LIST = enums.AlligatorTfsTuple(
            self.FAST, self.MIDDLE, self.LONG, self.VLONG
        )


config = Config()


if __name__ == "__main__":
    assert (
        enums.TIMEFRAMES["3m"] < enums.TIMEFRAMES["15m"] < enums.TIMEFRAMES["1h"]
    ), f'correct: {enums.TIMEFRAMES["3m"]} < {enums.TIMEFRAMES["15m"]} < {enums.TIMEFRAMES["1h"]}'
    assert (
        enums.TIMEFRAMES["3m"] < enums.TIMEFRAMES["1h"] < enums.TIMEFRAMES["15m"]
    ), f'Incorrect sequence of timeframes: {enums.TIMEFRAMES["3m"]} < {enums.TIMEFRAMES["1h"]} < {enums.TIMEFRAMES["15m"]}'
    print(enums.TIMEFRAMES["3m"])
