from pydantic import BaseModel
from typing import List, Dict, Tuple

from _logger import logger
from enums import AlligatorStatePool, AlligatorTfsTuple, StateEnum, AlligatorValuesPool
from indicators.alligator import Alligator
from indicators.indicator import Indicator
from models import Symbol, Timeframe
from strategies.abstract_strategy import AbstractSpotStrategy
from trader import Trader


class Strategy(AbstractSpotStrategy, BaseModel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.symbols_list: List[Symbol] = self._init_symbols(self.config.SYMBOLS_LIST)
        self.tfs: AlligatorTfsTuple = self.config.TIMEFRAMES_LIST
        self.indicators: List[Indicator] = [Alligator]

        self.trader = Trader(cfg=self.config)
        # account Basic Asset.
        self.basic_asset = self.config.BASE_COIN

        self.symbols: List[Symbol] = []

    def symbols_filter(self):
        for symbol in self.symbols_list:
            self.data_ctrl.start(
                (symbol.lower(), self.tfs.vlong),
                self.indicators[0](
                    symbol=symbol,
                    timeframe=Timeframe(name=self.tfs.vlong),
                ),
            )
            alligator = self.data_ctrl.getIndicator((symbol.lower(), self.tfs.vlong))
            if alligator.direction().value >= 1:
                logger.info(f"Working pair: ({symbol.name}, {self.tfs.vlong})")
                self.symbols.append(symbol)
            else:
                logger.info(
                    f"Detached: ({symbol.name}, {self.tfs.vlong}) -----------------------"
                )
                self.data_ctrl.stop((symbol.lower(), self.tfs.vlong))

    def init_data_ctrl(self):
        self.symbols_filter()

        logger.warning("List working pairs completed")
        logger.warning(f"START full work with {len(self.symbols)} pairs")
        logger.info(self.symbols.__str__())

        self.data_ctrl.init(self.symbols, self.tfs, self.indicators)

    def scout(self):
        recommend_buy = []
        recommend_sell = []
        for symbol in self.symbols:
            long = self._long_direction(symbol.lower())
            short = self._short_direction(symbol.lower())
            # states = self._get_states(symbol.lower())
            # recom = self._recommend(states)
            if long + short == 2:
                if self._volume(symbol.lower()):
                    logger.info(
                        f"BINGO BUY: {symbol} "
                        f"{self.data_ctrl.get((symbol.lower(), self.tfs.long))[0].last_price}"
                    )
                    recommend_buy.append(symbol)
                else:
                    logger.info(f"ALLIGATORS BUY: {symbol} " f"but volumes dont match")
            elif long + short == -2:
                if self._volume(symbol.lower()):
                    logger.info(
                        f"BINGO SELL: {symbol} "
                        f"{self.data_ctrl.get((symbol.lower(), self.tfs.vlong))[0].last_price}"
                    )
                    recommend_sell.append(symbol)
                else:
                    logger.info(f"ALLIGATORS SELL: {symbol} " f"but volumes dont match")
            else:
                pass

        if recommend_buy:
            logger.info(f"recommend_buy: {recommend_buy}")
        if recommend_sell:
            logger.info(f"recommend_sell: {recommend_sell}")

    def track(self):
        pass

    def _init_symbols(self, symbols: List[str]) -> List[Symbol]:
        return [Symbol(name=s) for s in symbols]

    def _get_states(self, symbol: str) -> AlligatorStatePool:
        # fast, middle, long - is Alligator
        fast = self.data_ctrl.get((symbol, self.tfs.fast))[1]
        middle = self.data_ctrl.get((symbol, self.tfs.middle))[1]
        long = self.data_ctrl.get((symbol, self.tfs.long))[1]
        vlong = self.data_ctrl.get((symbol, self.tfs.vlong))[1]
        return AlligatorStatePool(
            symbol, fast.state(), middle.state(), long.state(), vlong.state()
        )

    def _get_values(self, symbol: str, idx: int = 0) -> AlligatorValuesPool:
        # fast, middle, long - is Alligator
        fast = self.data_ctrl.get((symbol, self.tfs.fast))[1]
        middle = self.data_ctrl.get((symbol, self.tfs.middle))[1]
        long = self.data_ctrl.get((symbol, self.tfs.long))[1]
        vlong = self.data_ctrl.get((symbol, self.tfs.vlong))[1]
        return AlligatorValuesPool(
            symbol, fast.val(idx), middle.val(idx), long.val(idx), vlong.val(idx)
        )

    # def _get_volumes(self, symbol: str) -> VolumesPool:
    #     # fast, middle, long, vlong - is SymbolKline
    #     fast = self.data_ctrl.get((symbol, self.tfs.fast))[0]
    #     middle = self.data_ctrl.get((symbol, self.tfs.middle))[0]
    #     long = self.data_ctrl.get((symbol, self.tfs.long))[0]
    #     vlong = self.data_ctrl.get((symbol, self.tfs.vlong))[0]
    #     return VolumesPool(
    #         symbol,
    #     )

    def _recommend(self, states: AlligatorStatePool) -> int:
        ste = StateEnum
        if (
            all(
                (
                    ste[states.fast.lips].value >= ste.EAGLE.value,
                    ste[states.fast.teeth].value >= ste.GENTLE.value,
                    ste[states.fast.jaw].value >= ste.BREEZE.value,
                )
            )
            and all(
                (
                    ste[states.middle.lips].value >= ste.GENTLE.value,
                    ste[states.middle.teeth].value >= ste.GENTLE.value,
                    ste[states.middle.jaw].value >= ste.BREEZE.value,
                )
            )
            and all(
                (
                    ste[states.long.lips].value >= ste.GENTLE.value,
                    ste[states.long.teeth].value >= ste.BREEZE.value,
                    ste[states.long.jaw].value >= ste.FLAT.value,
                )
            )
        ):
            # logger.info(f'{states.name}_{self.tfs.fast}: {states.fast.lips} {states.fast.teeth} {states.fast.jaw}')
            # logger.info(
            #     f'{states.name}_{self.tfs.middle}: {states.middle.lips} {states.middle.teeth} {states.middle.jaw}')
            # logger.info(f'{states.name}_{self.tfs.long}: {states.long.lips} {states.long.teeth} {states.long.jaw}')
            return 1

        if (
            all(
                (
                    ste[states.fast.lips].value <= ste.CRASH.value,
                    ste[states.fast.teeth].value <= ste.DECLINE.value,
                    ste[states.fast.jaw].value <= ste.RETREAT.value,
                )
            )
            and all(
                (
                    ste[states.middle.lips].value <= ste.DECLINE.value,
                    ste[states.middle.teeth].value <= ste.DECLINE.value,
                    ste[states.middle.jaw].value <= ste.RETREAT.value,
                )
            )
            and all(
                (
                    ste[states.long.lips].value <= ste.DECLINE.value,
                    ste[states.long.teeth].value <= ste.RETREAT.value,
                    ste[states.long.jaw].value <= ste.FLAT.value,
                )
            )
        ):
            # logger.info(f'{states.name}_{self.tfs.fast}: {states.fast.lips} {states.fast.teeth} {states.fast.jaw}')
            # logger.info(
            #     f'{states.name}_{self.tfs.middle}: {states.middle.lips} {states.middle.teeth} {states.middle.jaw}')
            # logger.info(f'{states.name}_{self.tfs.long}: {states.long.lips} {states.long.teeth} {states.long.jaw}')
            return -1

        # logger.info(f'{states.name} neutral')
        return 0

    def _long_direction(self, symbol: str) -> int:
        _, fast, middle, long, vlong = self._get_values(symbol, idx=0)
        _, prev_fast, prev_middle, prev_long, prev_vlong = self._get_values(
            symbol, idx=1
        )
        last_price = self.data_ctrl.get((symbol, self.tfs.fast))[0].last_price
        ste = StateEnum

        # BUY direction
        buy_vlong_condition = all(
            (
                # правильная последовательность расположения МА Аллигатора
                last_price > vlong.lips.value > vlong.teeth.value > vlong.jaw.value,
                # vlong.xxx.value > prev_vlong.xxx.value - просто наклон вверх
                # чтобы учитывать степень наклона нужно использовать vlong.xxx.state
                vlong.teeth.value > prev_vlong.teeth.value,
                vlong.jaw.value > prev_vlong.jaw.value,
                ste[vlong.lips.state].value >= ste.FLAT.value,
            )
        )
        buy_long_condition = all(
            (
                # правильная последовательность расположения МА Аллигатора
                last_price > long.lips.value > long.teeth.value > long.jaw.value,
                # long.xxx.value > prev_long.xxx.value - просто наклон вверх
                # чтобы учитывать степень наклона необходимо использовать long.xxx.state
                long.teeth.value > prev_long.teeth.value,
                long.jaw.value > prev_long.jaw.value,
                ste[long.lips.state].value >= ste.FLAT.value,
            )
        )

        if all((buy_vlong_condition, buy_long_condition)):
            # logger.info(
            #     f'\nBUY {symbol} \n\t{vlong.lips.value} > {vlong.teeth.value} > {vlong.jaw.value}'
            #     f'\n\t{vlong.lips.state} {vlong.teeth.state} {vlong.jaw.state}'
            #     f'\n\t{long.lips.state} {long.teeth.state} {long.jaw.state}'
            # )
            return 1

        # SELL direction
        sell_vlong_condition = all(
            (
                # правильная последовательность расположения МА Аллигатора
                last_price < vlong.lips.value < vlong.teeth.value < vlong.jaw.value,
                # vlong.xxx.value < prev_vlong.xxx.value - просто наклон вниз
                # чтобы учитывать степень наклона нужно использовать vlong.xxx.state
                vlong.teeth.value < prev_vlong.teeth.value,
                vlong.jaw.value < prev_vlong.jaw.value,
                ste[vlong.lips.state].value <= ste.FLAT.value,
            )
        )
        sell_long_condition = all(
            (
                # правильная последовательность расположения МА Аллигатора
                last_price < long.lips.value < long.teeth.value < long.jaw.value,
                # long.xxx.value < prev_long.xxx.value - просто наклон вниз
                # чтобы учитывать степень наклона необходимо использовать long.xxx.state
                long.teeth.value < prev_long.teeth.value,
                long.jaw.value < prev_long.jaw.value,
                ste[vlong.lips.state].value <= ste.FLAT.value,
            )
        )

        if all((sell_vlong_condition, sell_long_condition)):
            # logger.info(
            #     f'\nSELL {symbol} \n\t{last_price} < {vlong.lips.value} < {vlong.teeth.value} < {vlong.jaw.value}'
            #     f'\n\t{vlong.lips.state} {vlong.teeth.state} {vlong.jaw.state}'
            #     f'\n\t{long.lips.state} {long.teeth.state} {long.jaw.state}'
            # )
            return -1

        # logger.info(f'{symbol} LONG condition NEUTRAL')
        return 0

    def _short_direction(self, symbol: str) -> int:
        _, fast, middle, long, vlong = self._get_values(symbol, idx=0)
        _, prev_fast, prev_middle, prev_long, prev_vlong = self._get_values(
            symbol, idx=1
        )
        last_price = self.data_ctrl.get((symbol, self.tfs.fast))[0].last_price
        ste = StateEnum

        # BUY direction
        buy_middle_condition = all(
            (
                # правильная последовательность расположения МА Аллигатора
                last_price > middle.lips.value > middle.teeth.value > middle.jaw.value,
                # middle.xxx.value > prev_middle.xxx.value - просто наклон вверх
                # чтобы учитывать степень наклона нужно использовать middle.xxx.state
                middle.teeth.value > prev_middle.teeth.value,
                middle.jaw.value > prev_middle.jaw.value,
                ste[middle.lips.state].value >= ste.BREEZE.value,
            )
        )
        buy_fast_condition = all(
            (
                # правильная последовательность расположения МА Аллигатора
                last_price > fast.lips.value > fast.teeth.value > fast.jaw.value,
                # fast.xxx.value > prev_fast.xxx.value - просто наклон вверх
                # чтобы учитывать степень наклона необходимо использовать fast.xxx.state
                # fast.teeth.value > prev_fast.teeth.value,
                # fast.jaw.value > prev_fast.jaw.value,
                ste[fast.lips.state].value >= ste.EAGLE.value,
                ste[fast.teeth.state].value >= ste.GENTLE.value,
                ste[fast.jaw.state].value >= ste.BREEZE.value,
            )
        )

        if all((buy_middle_condition, buy_fast_condition)):
            # logger.info(
            #     f'\nBUY {symbol} \n\t{last_price} > {middle.lips.value} > {middle.teeth.value} > {middle.jaw.value}'
            #     f'\n\t{middle.lips.state} {middle.teeth.state} {middle.jaw.state}'
            #     f'\n\t{fast.lips.state} {fast.teeth.state} {fast.jaw.state}'
            # )
            return 1

        # SELL Condition
        sell_middle_condition = all(
            (
                # правильная последовательность расположения МА Аллигатора
                last_price < middle.lips.value < middle.teeth.value < middle.jaw.value,
                # middle.xxx.value < prev_middle.xxx.value - просто наклон вниз
                # чтобы учитывать степень наклона необходимо использовать middle.xxx.state
                middle.teeth.value < prev_middle.teeth.value,
                middle.jaw.value < prev_middle.jaw.value,
                ste[middle.lips.state].value < ste.FLAT.value,
            )
        )
        sell_fast_condition = all(
            (
                # правильная последовательность расположения МА Аллигатора
                last_price < fast.lips.value < fast.teeth.value < fast.jaw.value,
                # fast.xxx.value < prev_fast.xxx.value - просто наклон вниз
                # чтобы учитывать степень наклона необходимо использовать fast.xxx.state
                # fast.teeth.value < prev_fast.teeth.value,
                # fast.jaw.value < prev_fast.jaw.value,
                ste[fast.lips.state].value <= ste.CRASH.value,
                ste[fast.teeth.state].value <= ste.DECLINE.value,
                ste[fast.jaw.state].value <= ste.RETREAT.value,
            )
        )

        if all((sell_middle_condition, sell_fast_condition)):
            # logger.info(
            #     f'\nSELL {symbol} \n\t{last_price} < {middle.lips.value} < {middle.teeth.value} < {middle.jaw.value}'
            #     f'\n\t{middle.lips.state} {middle.teeth.state} {middle.jaw.state}'
            #     f'\n\t{fast.lips.state} {fast.teeth.state} {fast.jaw.state}'
            # )
            return -1

        # logger.info(f'{symbol} SHORT condition NEUTRAL')
        return 0

    def _volume(self, symbol) -> bool:
        long = self.data_ctrl.get((symbol, self.tfs.long))[0]

        return any(
            (long.now_volume > long.now_mavolume, long.last_volume > long.last_mavolume)
        )


if __name__ == "__main__":
    pass
