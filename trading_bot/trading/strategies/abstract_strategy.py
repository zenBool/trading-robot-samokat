from abc import ABC, abstractmethod
from typing import List, Any

from pydantic import BaseModel

from trading.core.config import Config
from trading.core.data_controller import DataController
from trading.core.trader import Trader
from trading.indicators.indicator import Indicator
from trading.models import Symbol, Timeframe


class AbstractSpotStrategy(BaseModel, ABC):
    config: Config
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
