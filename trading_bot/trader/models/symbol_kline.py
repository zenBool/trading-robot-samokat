import time
from typing import Any, Dict

import pandas as pd
from pydantic import computed_field

import enums
from _logger import logger
from models import Timeframe, Symbol
from models.container import Container
from util import streamdata_to_dataframe


class SymbolKline(Container):
    symbol: str | Symbol
    timeframe: str | Timeframe
    values: pd.DataFrame | None
    _last_update: int = int(time.time() * 1000)
    _period_mavolumes: int = 13

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        if isinstance(self.symbol, str):
            self.symbol = Symbol(name=self.symbol)

        if isinstance(self.timeframe, str):
            self.timeframe = Timeframe(name=self.timeframe)

        self._calculate_mavolumes()

    def _calculate_mavolumes(self):
        mavolumes = []
        previous_mavolume = self.values.iloc[0]["volume"]
        for volume in self.values["volume"].to_list():
            new_mavolume = volume * self.k + previous_mavolume * (1 - self.k)
            mavolumes.append(new_mavolume)
            previous_mavolume = new_mavolume

        self.values = self.values.assign(mavolume=mavolumes)

    @computed_field
    @property
    def name(self) -> str:
        return f"{self.symbol.name}_{self.timeframe.name}"

    # @computed_field
    @property
    def k(self):
        # 'k' - coefficient for EMA moving
        return 2 / (self._period_mavolumes + 1)

    @property
    def last_price(self):
        return self.values["close"].iloc[-1]

    @property
    def now_volume(self):
        return self.values["volume"].iloc[-1]

    @property
    def last_volume(self):
        return self.values["volume"].iloc[-2]

    @property
    def prev_volume(self):
        return self.values["volume"].iloc[-3]

    @property
    def now_mavolume(self):
        return self.values["mavolume"].iloc[-1]

    @property
    def last_mavolume(self):
        return self.values["mavolume"].iloc[-2]

    @property
    def prev_mavolume(self):
        return self.values["mavolume"].iloc[-3]

    def min_num_bars(self, bars: int):
        return self.values["low"].iloc[-bars:].min()

    def max_num_bars(self, bars: int):
        return self.values["high"].iloc[-bars:].max()

    def update(self, data: Dict):
        if data["i"] == "1m":
            data = self._update_from_1m(data)
        elif data["i"] != self.timeframe.name:
            logger.error(f"Wrong timeframe: {data['i']}")
            exit(1)
        df: pd.DataFrame
        try:
            df = streamdata_to_dataframe(data)
        except Exception as e:
            logger.error(f"DataManager: Don't update stream \n{e} ")

        t = df.index[0]

        try:
            if t not in self.values.index:
                if t != (self.values.index.max() + self.timeframe.ms):
                    # исключение заменить загрузкой пропущенных баров
                    logger.error(
                        f"Destroyed data continuity before: {pd.to_datetime(t, unit='ms')}"
                    )
                    logger.error(
                        f"Last row in kline: {self.values.index.max()} new data: {t}"
                    )
                    raise
                else:
                    df["mavolume"] = (
                        df["volume"] * self.k
                        + (1 - self.k) * self.values.iloc[-1]["mavolume"]
                    )
                    self.values = pd.concat([self.values, df])
            else:
                df["mavolume"] = (
                    df["volume"] * self.k
                    + (1 - self.k) * self.values.iloc[-2]["mavolume"]
                )
                self.values.update(df)
        except Exception as e:
            logger.error(e)

        _ = self.last_update

    def _update_from_1m(self, data: Dict) -> Dict:
        last_index = self.values.index.max()
        if last_index < data["t"] < last_index + self.timeframe.ms - 1:
            # это не первая минута текущей свечи
            data["t"] = last_index
            data["T"] = last_index + self.timeframe.ms - 1
            data["h"] = str(max(float(data["h"]), self.values.loc[last_index, "high"]))
            data["l"] = str(min(float(data["l"]), self.values.loc[last_index, "low"]))
            if data["x"]:
                data["v"] = str(
                    float(data["v"]) + self.values.loc[last_index, "volume"]
                )
                # проверка подсчета объема при обновлении из 1м
                # if data['T'] == last_index + self.timeframe.ms - 1:
                #     logger.info(f"Total volume on bar: {data['v']}")

                return data
            else:
                data["v"] = str(self.values.loc[last_index, "volume"])
                return data

        if data["t"] == last_index + self.timeframe.ms or data["t"] == last_index:
            # это первая минута существующей или новой свечи, поэтому меняем только время закрытия свечи
            data["T"] = data["t"] + self.timeframe.ms - 1
            return data

        raise RuntimeError(f"Ошибка обработки данных {data}")


if __name__ == "__main__":
    from binance.spot import Spot as Client
    import pandas as pd

    client = Client()  # base_url="https://testnet.binance.vision"
    symb = Symbol(name="BTCUSDT")
    tf = Timeframe(name="1h")
    data = client.klines(symb.name, tf.name, limit=500)
    df = pd.DataFrame(data, columns=enums.COLUMNS.keys()).astype(
        enums.COLUMNS, copy=False
    )
    df.set_index(df["time_open"], inplace=True)
    df.index.name = None

    s = SymbolKline(symbol=symb, timeframe=tf, values=df)

    logger.info(s.values[["volume", "mavolume"]].tail())
    # logger.info(s.values.dtypes)
    # logger.info(s.values['mavolume'].iloc[-1])
