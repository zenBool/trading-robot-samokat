import json
import time
from datetime import datetime
from typing import List, Dict, Tuple

import pandas as pd
from pydantic import BaseModel

import enums
from enums import AlligatorTfsTuple
from _logger import logger
from clients import Client, WSStreamClient

from indicators.indicator import Indicator
from models import Timeframe, Symbol, SymbolKline
from storage import Storage
from util import streamdata_to_dataframe


class DataController(BaseModel):
    storage: Storage
    client: Client | None = None
    ws_client: WSStreamClient | None = None
    symbols: List[Symbol] | List[str] = []
    timeframes: AlligatorTfsTuple = ()
    indicators: List[Indicator] = []
    _streams_id: Dict = {}

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # оба клиента не нуждаются в Ключах
        self.client = Client()
        self.ws_client = WSStreamClient(message_handler=self._handler)

    def init(self, symbols: List[Symbol], timeframes, indicators):
        self.symbols = symbols
        self.timeframes = timeframes
        self.indicators = indicators
        for symb in self.symbols:
            for tf in self.timeframes:
                name = (symb.lower(), tf)

                if name in self.storage.list_klines:
                    logger.info(
                        f"----------------------------Stream {name} already in Storage KLINES"
                    )
                    continue
                if name in self.storage.list_indicators:
                    logger.info(
                        f"--------------Stream {name} already in Storage INDICATORS"
                    )
                    continue

                for ind in self.indicators:
                    alligator = ind(symbol=symb, timeframe=Timeframe(name=tf))
                    self.start(name, alligator)

    def start(self, name: Tuple[str, str], indicator: Indicator):
        self.storage.add(name, indicator)
        self._load_data(name)

    def stop(self, name: Tuple[str, str] | None = None):
        if not name:
            self.ws_client.stop()
        else:
            try:
                if name not in self._streams_id.keys():
                    return
                self.ws_client.stop(id=self._streams_id.pop(name))
                self.storage.delete(name)
                logger.info(f"Stream {name} stopped")
            except Exception as e:
                logger.error(f"DataManager: Don't stop stream {name}\n{e}")

    # def update(self, name: Tuple[str, str], data: pd.DataFrame):
    #     self.storage.update(name, data)

    def get(self, name: Tuple[str, str]) -> Tuple[SymbolKline, Indicator] | None:
        return self.storage.get(name)

    def getSymbolKline(self, name: Tuple[str, str]) -> SymbolKline | None:
        """
        Retrieves symbol kline for the given name and returns it, or returns None if it does not exist.
        Parameters:
            name (Tuple[str, str]): The name of the symbol.
        Returns:
            Union[SymbolKline, None]: The symbol kline or None if it does not exist.
        """
        return self.storage.get_kline(name)

    def getIndicator(self, name: Tuple[str, str]) -> Indicator | None:
        return self.storage.get_indicator(name)

    @property
    def streams_list(self) -> List[Tuple[str, str]]:
        return sorted(self.storage.list_klines)

    def _handler(self, socketManager, message):
        """
        Обработчик стрим-данных

        :param socketManager:
        :param message:
        :return:
        """

        msg = json.loads(message)
        if "stream" not in msg:
            print("waiting")
            return

        # data = {
        #             "t": 123400000, // Kline start time
        #             "T": 123460000, // Kline close time
        #             "s": "BNBBTC",  // Symbol
        #             "i": "1m",      // Interval
        #             "f": 100,       // First trade ID
        #             "L": 200,       // Last trade ID
        #             "o": "0.0010",  // Open price
        #             "c": "0.0020",  // Close price
        #             "h": "0.0025",  // High price
        #             "l": "0.0015",  // Low price
        #             "v": "1000",    // Base asset volume
        #             "n": 100,       // Number of trades
        #             "x": false,     // Is this kline closed?
        #             "q": "1.0000",  // Quote asset volume
        #             "V": "500",     // Taker buy base asset volume
        #             "Q": "0.500",   // Taker buy quote asset volume
        #             "B": "123456"   // Ignore
        #         }
        data = msg["data"]["k"]

        symbol_ = msg["stream"].split("@")[0]
        for tf in self.timeframes:
            symbol_tf = (symbol_, tf)
            # Обновление SymbolKline
            self.storage.update(symbol_tf, data)
            # Обновление Indicator
            df = streamdata_to_dataframe(data)
            self.storage.update(symbol_tf, df)

    def _load_kline(
        self, symbol: str, timeframe: str, limit: int = 1000
    ) -> SymbolKline:
        try:
            kline = self.client.klines(symbol.upper(), timeframe, limit=limit)
        except Exception as e:
            logger.error(f"DataManager: Don't load kline {symbol} {timeframe}")
            logger.error(e)
            exit(1)
        df = pd.DataFrame(kline, columns=enums.COLUMNS.keys()).astype(
            enums.COLUMNS, copy=False
        )
        df.set_index(df["time_open"], inplace=True)
        df.index.name = None

        return SymbolKline(symbol=symbol, timeframe=timeframe, values=df)

    def _load_data(self, name: Tuple[str, str]):
        """Load data from Binance API and calculate indicators
        :param name: tuple(symbol, timeframe)
        :return: None

        """

        logger.info(f"Start load {name} {datetime.now()}")

        symbolkline: SymbolKline = self._load_kline(*name)
        logger.info(f"Finish load {name} {datetime.now()}")
        # while not symbolkline.values.empty:
        #     time.sleep(0.3)
        self.storage.add(name, symbolkline)
        logger.info(f"Load {symbolkline.name}")

        indicator = self.storage.get_indicator(name)
        indicator.calculate(symbolkline.values)
        logger.info(f"Calculate {self.storage.get_indicator(name).name}")

        # start stream for symbol_kline
        if (name[0], "1m") not in self._streams_id:
            t = int(time.time() * 1000)
            self.ws_client.kline(
                symbol=name[0],
                interval="1m",
                # interval=name[1],
                id=t,
            )
            self._streams_id[(name[0], "1m")] = t


if __name__ == "__main__":
    pass
