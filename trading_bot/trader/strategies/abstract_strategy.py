from abc import ABC, abstractmethod
from typing import List, Any

from pydantic import BaseModel

from cfg import Cfg
from data_controller import DataController
from indicators.indicator import Indicator
from models import Timeframe, Symbol
from trader import Trader


class AbstractSpotStrategy(BaseModel, ABC):
    config: Cfg
    data_ctrl: DataController
    trader: Trader | None = None
    basic_asset: str | None = "USDT"
    symbols_list: List[str] | None = None
    symbols: List[str | Symbol] | None = None
    tfs: List[str | Timeframe] | None = None
    indicators: List[Indicator] | None = None
    assets: List[Any] | None = None

    class Config:
        arbitrary_types_allowed = True

    @abstractmethod
    def scout(self):
        pass

    @abstractmethod
    def track(self):
        pass


if __name__ == "__main__":
    pass
