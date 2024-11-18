from datetime import datetime, timezone
from collections import namedtuple
from enum import Enum
from typing import Dict

import pandas as pd
from pydantic import computed_field, BaseModel
from sqlalchemy.engine import Engine

from _logger import logger
from enums import ValuesMA
from indicators.indicator import Indicator
from models import Symbol, Timeframe


def percentile(symbol: str, timeframe: str, _engine: Engine) -> pd.DataFrame:
    prcntl = pd.read_sql_table(f'prcntl_{symbol.lower()}_{timeframe}', _engine)
    return prcntl


class MovingAverage(Indicator):
    symbol: str | Symbol
    timeframe: str | Timeframe
    period: int = 1
    ma_type: str = 'EMA'
    slope: Enum | None = None

    def __init__(self, **kwargs):
        if isinstance(kwargs['symbol'], str):
            kwargs['symbol'] = Symbol(name=kwargs['symbol'])
        if isinstance(kwargs['timeframe'], str):
            kwargs['timeframe'] = Timeframe(name=kwargs['timeframe'])
        super().__init__(**kwargs)
        self._set_slope()

    @computed_field
    @property
    def name(self) -> str:
        return f'{self.symbol.name}_{self.timeframe.name}_{self.ma_type}_{self.period}'.lower()

    def val(self, idx: int) -> ValuesMA:
        """
        idx указывает на бар, которые сортированы в обратном хронологическом порядке.
        0 - текущий бар, 1 - предыдущий бар и т.д.
        :param idx: номер бара от текущего. 0 - текущий бар
        :return: namedtuple('ValuesMA', ['time', 'value', 'delta', 'state'])
        """
        if idx < 0:
            logger.error(f'Index {idx} is less than 0')
            raise IndexError

        row = self.values.iloc[-idx - 1]

        ms = self.values.iloc[-idx - 1].name
        # index - время в удобочитаемом виде
        index = datetime.fromtimestamp(ms / 1000, tz=timezone.utc).strftime('%Y-%m-%d %H:%M')

        # return ValueDelta(*row)
        return ValuesMA(index, *row)

    def state(self, value: float) -> str:
        if value > self.slope.FLAT.value:
            if value > self.slope.FRENZY.value:
                return 'FRENZY'
            elif value > self.slope.EAGLE.value:
                return 'EAGLE'
            elif value > self.slope.GENTLE.value:
                return 'GENTLE'
            elif value > self.slope.BREEZE.value:
                return 'BREEZE'
            else:
                return self.slope.FLAT.name
        else:
            if value < self.slope.PANIC.value:
                return 'PANIC'
            elif value < self.slope.CRASH.value:
                return 'CRASH'
            elif value < self.slope.DECLINE.value:
                return 'DECLINE'
            elif value < self.slope.RETREAT.value:
                return 'RETREAT'
            else:
                return self.slope.FLAT.name

    def calculate(self, candles: pd.DataFrame):
        values_ma = []
        delta_ma = []
        state_ma = []
        # 'k' - for EMA moving
        k = 2 / (self.period + 1)
        previous_ma = candles.iloc[0]['close']
        for close in candles['close'].to_list():
            new_ema = close * k + previous_ma * (1 - k)
            values_ma.append(new_ema)
            delta = round((new_ema / previous_ma - 1) * 100, 5)
            delta_ma.append(delta)
            state_ma.append(self.state(delta))
            previous_ma = new_ema

        col = f'ema_{self.period}'
        delta = f'ma_{self.period}_delta'
        state = f'ma_{self.period}_state'
        self.values = pd.DataFrame(
            data={col: values_ma, delta: delta_ma, state: state_ma},
            index=candles.index
        ).astype({col: 'float', delta: 'float', state: 'str'})

    def update(self, data: pd.DataFrame | Dict):

        t = data.index[0]
        # 'k' - for EMA moving
        k = 2 / (self.period + 1)
        col = f'ema_{self.period}'
        delta = f'ma_{self.period}_delta'
        state = f'ma_{self.period}_state'
        if t not in self.values.index:
            if t != (self.values.index.max() + self.timeframe.ms):
                # исключение заменить загрузкой пропущенных баров
                logger.error(f"Destroyed data continuity before: {pd.to_datetime(t, unit='ms')} == {t}")
                logger.error(f'Last row in kline: {self.values.index.max()}\nnew data: {t}')
                raise
            else:
                previous_ma = self.values.iloc[-1][col]
                ma = data.iloc[0]['close'] * k + previous_ma * (1 - k)
                delta_ma = round((ma / previous_ma - 1) * 100, 5)
                state_ma = self.state(delta_ma)
                df = pd.DataFrame({col: [ma], delta: [delta_ma], state: [state_ma]}, index=[t])
                self.values = pd.concat([self.values, df])
                _ = self.last_update
        else:
            previous_ma = self.values.iloc[-2][col]
            ma = data.iloc[0]['close'] * k + previous_ma * (1 - k)
            delta_ma = round((ma / previous_ma - 1) * 100, 5)
            state_ma = self.state(delta_ma)
            try:
                # self.values.iloc[-1, col] = ma
                # self.values.iloc[-1, delta] = delta_ma
                # self.values.iloc[-1, state] = state_ma
                idx = self.values.index[-1]
                self.values.at[idx, col] = ma
                self.values.at[idx, delta] = delta_ma
                self.values.at[idx, state] = state_ma
            except Exception as e:
                logger.error(f"values.iloc bad index in {self.name} {e}")
            _ = self.last_update

    def _update_from_dict(self, data: Dict):
        pass

    def _set_slope(self):
        from db._get_engine import get_engine
        # Получаем percentile из базы данных
        df = percentile(self.symbol.name, self.timeframe.name, get_engine())

        # имя столбца периода скользящей средней
        column_name = f'ma_{self.period}_delta'

        # Выбираем значения для каждого поля в self.slope
        slope = {
            'FRENZY': df.loc[df['index'] == '95%', column_name].values[0],
            'EAGLE': df.loc[df['index'] == '90%', column_name].values[0],
            'GENTLE': df.loc[df['index'] == '80%', column_name].values[0],
            'BREEZE': df.loc[df['index'] == '70%', column_name].values[0],
            'FLAT': df.loc[df['index'] == '50%', column_name].values[0],
            'RETREAT': df.loc[df['index'] == '30%', column_name].values[0],
            'DECLINE': df.loc[df['index'] == '20%', column_name].values[0],
            'CRASH': df.loc[df['index'] == '10%', column_name].values[0],
            'PANIC': df.loc[df['index'] == '5%', column_name].values[0],
        }
        self.slope = Enum('Slope', slope)


if __name__ == '__main__':
    tup = [('BTCUSDT', '1h'), ('BTCUSDT', '15m'), ('BTCUSDT', '5m')]
    symlist = []
    tflist = []
    for sym, tf in tup:
        symlist.append(sym)
        tflist.append(tf)

    for s in symlist:
        for t in tflist:
            print(s)
            if (s, t) not in [('ETHUSDT', '1h'), ('ETHUSDT', '15m'), ('ETHUSDT', '5m')]:
                print('break')
                break
            print(t)
    
