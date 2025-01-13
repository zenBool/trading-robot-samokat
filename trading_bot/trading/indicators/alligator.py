import pandas as pd
from pydantic import Field

from trading.enums.enums import AlligatorState, AlligatorValues, EnumAlligatorDirection, StateEnum
from trading.indicators.indicator import Indicator
from trading.indicators.moving_average import MovingAverage


class Alligator(Indicator):
    lips: int = Field(gt=0, default=5)
    teeth: int = Field(gt=0, default=13)
    jaw: int = Field(gt=0, default=34)

    lips_ma: MovingAverage | None = None
    teeth_ma: MovingAverage | None = None
    jaw_ma: MovingAverage | None = None

    class Config:
        arbitrary_types_allowed = True

    @property
    def name(self) -> str:
        if self.symbol and self.timeframe:
            return f'{self.symbol.name}_{self.timeframe.name}_alligator_{self.lips}_{self.teeth}_{self.jaw}'.lower()
        else:
            return f'none_none_alligator_{self.lips}_{self.teeth}_{self.jaw}'.lower()

    def calculate(self, df: pd.DataFrame):
        """
        Расчет Аллигатора "с нуля"
        :param df:
        :return:
        """
        self.lips_ma = MovingAverage(
            symbol=self.symbol,
            timeframe=self.timeframe,
            period=self.lips
        )
        self.lips_ma.calculate(df)

        self.teeth_ma = MovingAverage(
            symbol=self.symbol,
            timeframe=self.timeframe,
            period=self.teeth
        )
        self.teeth_ma.calculate(df)

        self.jaw_ma = MovingAverage(
            symbol=self.symbol,
            timeframe=self.timeframe,
            period=self.jaw
        )
        self.jaw_ma.calculate(df)

    def val(self, idx: int) -> AlligatorValues:
        lips = self.lips_ma.val(idx)  # '.val()' is namedtuple['time', 'value', 'delta', 'state']
        teeth = self.teeth_ma.val(idx)
        jaw = self.jaw_ma.val(idx)
        return AlligatorValues(
            name=self.name,
            lips=lips,
            teeth=teeth,
            jaw=jaw
        )

    def total(self) -> pd.DataFrame:
        return pd.concat([self.lips_ma.values, self.teeth_ma.values, self.jaw_ma.values], axis=1)

    def update(self, data: pd.DataFrame):
        self.lips_ma.update(data)
        self.teeth_ma.update(data)
        self.jaw_ma.update(data)

    def state(self, idx: int = 0) -> AlligatorState:
        row_lips = self.lips_ma.val(idx)  # '.val()' is namedtuple['time', 'value', 'delta', 'state']
        row_teeth = self.teeth_ma.val(idx)
        row_jaw = self.jaw_ma.val(idx)
        return AlligatorState(self.name,
                              row_lips.state,
                              row_teeth.state,
                              row_jaw.state
                              )

    def direction(self, idx: int = 0) -> EnumAlligatorDirection:
        #
        # lips, teeth, jaw  is namedtuple['time', 'value', 'delta', 'state']
        #
        #
        _, lips, teeth, jaw = self.val(idx)
        # _, lips_prev, teeth_prev, jaw_prev = self.val(idx + 1)
        if all((
            StateEnum[teeth.state].value > StateEnum.FLAT.value,
            StateEnum[jaw.state].value > StateEnum.FLAT.value,
            lips.value > teeth.value > jaw.value,
        )):
            if StateEnum[lips.state].value > StateEnum.FLAT.value:
                return EnumAlligatorDirection.UP
            else:
                return EnumAlligatorDirection.UPCORRECTION
        elif all((
            StateEnum[teeth.state].value < StateEnum.FLAT.value,
            StateEnum[jaw.state].value < StateEnum.FLAT.value,
            lips.value < teeth.value < jaw.value,
        )):
            if StateEnum[lips.state].value < StateEnum.FLAT.value:
                return EnumAlligatorDirection.DOWN
            else:
                return EnumAlligatorDirection.DOWNCORRECTION
        else:
            return EnumAlligatorDirection.UNCERTAIN


if __name__ == '__main__':
    print(StateEnum['FRENZY'].value)
