import time
from abc import ABC, abstractmethod
from typing import Dict

import pandas as pd

from pydantic import BaseModel, computed_field

from trading.models import Symbol, Timeframe


class Container(BaseModel, ABC):
    symbol: str | Symbol | None = None
    timeframe: str | Timeframe | None = None
    values: pd.DataFrame | None = None
    _last_update: int = -1

    class Config:
        arbitrary_types_allowed = True

    @computed_field
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def update(self, data: Dict | pd.DataFrame):
        pass

    @property
    def last_update(self):
        res = self._last_update
        self._last_update = int(time.time() * 1000)
        return res


if __name__ == '__main__':
    pass
