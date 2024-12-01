import pandas as pd
from pydantic import BaseModel
from typing import Tuple, Dict

from common.logger import logger
from common.singleton import Singleton

from trading.indicators.indicator import Indicator
from trading.models import SymbolKline


class Storage(Singleton, BaseModel):
    """Класс хранит данные в наследниках SymbolKline.
    Умеет добавлять, удалять данные в хранилище
    Обновление дилегируется хранимому типу
    self.list() - отдает множество имен всех, находящихся в хранилище, данных SymbolKline.name
    """

    _indicators: Dict[Tuple[str, str], Indicator] = {}
    _klines: Dict[Tuple[str, str], SymbolKline] = {}

    def __init__(self):
        super().__init__()
        self._logger = logger.getChild("Storage")

    def get(self, name: Tuple[str, str]) -> Tuple[SymbolKline, Indicator] | None:
        if name in self.list_klines:
            return self.get_kline(name), self.get_indicator(name)
        else:
            self._logger.warning(f"Data {name} not exist in the STORAGE")
            # raise
            return None

    def get_indicator(self, name: Tuple[str, str]) -> Indicator | None:
        if name in self._indicators.keys():
            return self._indicators[name]
        else:
            self._logger.warning(f"Data {name} not exist in the STORAGE")
            # raise
            return None

    def get_kline(self, name: Tuple[str, str]) -> SymbolKline | None:
        if name in self._klines.keys():
            return self._klines[name]
        else:
            self._logger.warning(f"SymbolKline {name} not exist in the STORAGE")
            # raise
            return None

    def add(self, name: Tuple[str, str], data: Indicator | SymbolKline):
        if isinstance(data, Indicator):
            if name not in self._indicators.keys():
                self._indicators[name] = data
                self._logger.info(f"Indicator {name} added. 'data' is {type(data)}")
            else:
                self._logger.warning(f"Indicator {name} is exist in Store")
        elif isinstance(data, SymbolKline):
            if name not in self._klines.keys():
                self._klines[name] = data
            else:
                self._logger.warning(f"Kline {name} is exist in Store")
        else:
            self._logger.error(f"Storage.add() - error")

    def delete(self, name: Tuple[str, str]):
        try:
            _ = self._indicators.pop(name)
            _ = self._klines.pop(name)
        except KeyError as e:
            self._logger.warning(f"Can't delete {name}. Don't exist in STORAGE\n{e}")

    def update(self, name: Tuple[str, str], data: Dict | pd.DataFrame):
        if name in self.list_klines:
            if isinstance(data, pd.DataFrame):
                try:
                    self._indicators[name].update(data)
                except Exception as e:
                    self._logger.error(f"STORAGE: _indicators Don't update {name}\n{e}")
            elif isinstance(data, dict):
                try:
                    # logger.info(f"Kline {self._klines[name].name} {type(self._klines[name])}")
                    self._klines[name].update(data)
                    # logger.info(f"Kline {name} have {self._klines[name].values.shape} 'rows, column'")
                except Exception as e:
                    self._logger.error(f"STORAGE: _klines Don't update {name}\n{e}")
            else:
                self._logger.warning(f"Never may be type: {type(data)}.")

    def update_from_1m(self, name: Tuple[str, str], data: Dict):
        pass

    @property
    def list_klines(self) -> tuple[tuple[str, str], ...]:
        items = self._klines.keys()
        return tuple(items)

    @property
    def list_indicators(self) -> tuple[tuple[str, str], ...]:
        items = self._indicators.keys()
        return tuple(items)


if __name__ == "__main__":
    pass
1