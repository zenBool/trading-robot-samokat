from abc import ABC, abstractmethod

import pandas as pd

from models import Symbol, Timeframe
from models.container import Container


class Indicator(Container, ABC):
    symbol: str | Symbol | None = None
    timeframe: str | Timeframe | None = None
    values: pd.DataFrame | None = None
    _last_update: int = -1

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, **kwargs):
        if isinstance(kwargs['symbol'], str):
            kwargs['symbol'] = Symbol(name=kwargs['symbol'])
        if isinstance(kwargs['timeframe'], str):
            kwargs['timeframe'] = Timeframe(name=kwargs['timeframe'])
        super().__init__(**kwargs)

    @abstractmethod
    def state(self, **kwargs) -> str:
        ...

    @abstractmethod
    def calculate(self, kline: pd.DataFrame):
        ...

    @abstractmethod
    def val(self, idx: int):
        pass

    @property
    def now(self):
        return self.val(0)

    @property
    def last(self):
        return self.val(1)

    @property
    def prev(self):
        return self.val(2)


if __name__ == '__main__':
    pass
