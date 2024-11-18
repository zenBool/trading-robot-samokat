import pandas as pd
from pydantic import BaseModel
from typing import Tuple, Dict

from _logger import logger

from indicators.indicator import Indicator
from models import SymbolKline
from models.singleton import Singleton


class Storage(Singleton, BaseModel):
    """Класс хранит данные в наследниках SymbolKline.
    Умеет добавлять, удалять данные в хранилище
    Обновление дилегируется хранимому типу
    self.list() - отдает множество имен всех, находящихся в хранилище, данных SymbolKline.name
    """

    _indicators: Dict[Tuple[str, str], Indicator] = {}
    _klines: Dict[Tuple[str, str], SymbolKline] = {}

    def get(self, name: Tuple[str, str]) -> Tuple[SymbolKline, Indicator] | None:
        if name in self.list_klines:
            return self.get_kline(name), self.get_indicator(name)
        else:
            logger.warning(f"Data {name} not exist in the STORAGE")
            # raise
            return None

    def get_indicator(self, name: Tuple[str, str]) -> Indicator | None:
        if name in self._indicators.keys():
            return self._indicators[name]
        else:
            logger.warning(f"Data {name} not exist in the STORAGE")
            # raise
            return None

    def get_kline(self, name: Tuple[str, str]) -> SymbolKline | None:
        if name in self._klines.keys():
            return self._klines[name]
        else:
            logger.warning(f"SymbolKline {name} not exist in the STORAGE")
            # raise
            return None

    def add(self, name: Tuple[str, str], data: Indicator | SymbolKline):
        if isinstance(data, Indicator):
            if name not in self._indicators.keys():
                self._indicators[name] = data
                logger.info(f"Indicator {name} added. 'data' is {type(data)}")
            else:
                logger.warning(f"Indicator {name} is exist in Store")
        elif isinstance(data, SymbolKline):
            if name not in self._klines.keys():
                self._klines[name] = data
            else:
                logger.warning(f"Kline {name} is exist in Store")
        else:
            logger.error(f"Storage.add() - error")

    def delete(self, name: Tuple[str, str]):
        try:
            _ = self._indicators.pop(name)
            _ = self._klines.pop(name)
        except KeyError as e:
            logger.warning(f"Can't delete {name}. Don't exist in STORAGE\n{e}")

    def update(self, name: Tuple[str, str], data: Dict | pd.DataFrame):
        if name in self.list_klines:
            if isinstance(data, pd.DataFrame):
                try:
                    self._indicators[name].update(data)
                except Exception as e:
                    logger.error(f"STORAGE: _indicators Don't update {name}\n{e}")
            elif isinstance(data, dict):
                try:
                    # logger.info(f"Kline {self._klines[name].name} {type(self._klines[name])}")
                    self._klines[name].update(data)
                    # logger.info(f"Kline {name} have {self._klines[name].values.shape} 'rows, column'")
                except Exception as e:
                    logger.error(f"STORAGE: _klines Don't update {name}\n{e}")
            else:
                logger.warning(f"Never may be type: {type(data)}.")

    def update_from_1m(self, name: Tuple[str, str], data: Dict):
        pass

    @property
    def list_klines(self) -> Tuple[Tuple[str, str]]:
        items = self._klines.keys()
        return tuple(items)

    @property
    def list_indicators(self) -> Tuple[Tuple[str, str]]:
        items = self._indicators.keys()
        return tuple(items)


if __name__ == "__main__":
    pass
