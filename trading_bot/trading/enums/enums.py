from collections import namedtuple
from enum import Enum
from typing import Literal, List, Any

INTERVALS: List[str] = [
    "1s",
    "1m",
    "3m",
    "5m",
    "15m",
    "30m",
    "1h",
    "2h",
    "4h",
    "6h",
    "8h",
    "12h",
    "1d",
    "3d",
    "1w",
    "1M",
]
INTERVALS_LITERAL = Literal[
    "1s",
    "1m",
    "3m",
    "5m",
    "15m",
    "30m",
    "1h",
    "2h",
    "4h",
    "6h",
    "8h",
    "12h",
    "1d",
    "3d",
    "1w",
]
PERCENTILE: List[str] = [
    "count",
    "mean",
    "std",
    "min",
    "5%",
    "10%",
    "15%",
    "20%",
    "25%",
    "30%",
    "35%",
    "40%",
    "45%",
    "50%",
    "55%",
    "60%",
    "65%",
    "70%",
    "75%",
    "80%",
    "85%",
    "90%",
    "95%",
    "max",
]
TIMEFRAMES = {
    "1s": 1000,
    "1m": 1000 * 60,
    "3m": 1000 * 60 * 3,
    "5m": 1000 * 60 * 5,
    "15m": 1000 * 60 * 15,
    "30m": 1000 * 60 * 30,
    "1h": 1000 * 60 * 60,
    "2h": 1000 * 60 * 60 * 2,
    "4h": 1000 * 60 * 60 * 4,
    "6h": 1000 * 60 * 60 * 6,
    "8h": 1000 * 60 * 60 * 8,
    "12h": 1000 * 60 * 60 * 12,
    "1d": 1000 * 60 * 60 * 24,
    "3d": 1000 * 60 * 60 * 24 * 3,
    "1w": 1000 * 60 * 60 * 24 * 7,
    # "1M": 1000 * 60 * 60 * 24 * 30,  # 30 days. Didn't use in Strategy. May be receiving from kline stream
}

TRADING_TYPE = Literal["spot", "um", "cm"]
MONTHS = list(range(1, 13))
INTERVALS_TIME = {
    "1m": 1000 * 60,
    "3m": 1000 * 60 * 3,
    "5m": 1000 * 60 * 5,
    "15m": 1000 * 60 * 15,
    "30m": 1000 * 60 * 30,
    "1h": 1000 * 60 * 60,
    "2h": 1000 * 60 * 60 * 2,
    "4h": 1000 * 60 * 60 * 4,
    "6h": 1000 * 60 * 60 * 6,
    "8h": 1000 * 60 * 60 * 8,
    "12h": 1000 * 60 * 60 * 12,
    "1d": 1000 * 60 * 60 * 24,
    "3d": 1000 * 60 * 60 * 24 * 3,
    "1w": 1000 * 60 * 60 * 24 * 7,
}
# COLUMNS = ['time_open', 'open', 'high', 'low', 'close', 'volume', 'time_close', 'q_asset_vol',
#            'num_trades', 'tb_base_av', 'tb_quote_av', 'ignore']
COLUMNS = {
    "time_open": "int64",
    "open": "float",
    "high": "float",
    "low": "float",
    "close": "float",
    "volume": "float",
    "time_close": "int64",
    "q_asset_vol": "float",
    "num_trades": "int",
    "tb_base_av": "float",
    "tb_quote_av": "float",
    "ignore": "str",
}
STREAMKLINE_COLUMNS = [
    "t",
    "o",
    "h",
    "l",
    "c",
    "v",
    "T",
    "q",
    "n",
    "V",
    "Q",
    "B",
]  # dont change
COLUMNS_EMA = [
    "ma_5",
    "ma_8",
    "ma_13",
    "ma_21",
    "ma_34",
    "ma_55",
    "ma_89",
    "ma_144",
    "ma_5_delta",
    "ma_8_delta",
    "ma_13_delta",
    "ma_21_delta",
    "ma_34_delta",
    "ma_55_delta",
    "ma_89_delta",
    "ma_144_delta",
    "time_open",
]
SYMBOLS_100M = [
    "BTCUSDT",
    "ETHUSDT",
    "BNBUSDT",
    "LTCUSDT",
    "ADAUSDT",
    "XRPUSDT",
    "LINKUSDT",
    "FETUSDT",
    "MATICUSDT",
    "DOGEUSDT",
    "BCHUSDT",
    "SOLUSDT",
    "DOTUSDT",
    "RUNEUSDT",
    "AVAXUSDT",
    "NEARUSDT",
    "FILUSDT",
    "INJUSDT",
    "REEFUSDT",
    "SHIBUSDT",
    "GALAUSDT",
    "AMPUSDT",
    "RNDRUSDT",
    "OOKIUSDT",
    "OPUSDT",
    "HIFIUSDT",
    "IDUSDT",
    "ARBUSDT",
    "SUIUSDT",
    "PEPEUSDT",
    "FLOKIUSDT",
    "WLDUSDT",
    "SEIUSDT",
    "TIAUSDT",
    "ORDIUSDT",
    "VANRYUSDT",
    "1000SATSUSDT",
    "BONKUSDT",
    "PIXELUSDT",
    "STRKUSDT",
    "WIFUSDT",
]
SYMBOLS_50M = [
    "TRXUSDT",
    "ETCUSDT",
    "WAVESUSDT",
    "ZRXUSDT",
    "ATOMUSDT",
    "FTMUSDT",
    "ALGOUSDT",
    "HBARUSDT",
    "ARPAUSDT",
    "MKRUSDT",
    "SANDUSDT",
    "UNIUSDT",
    "GRTUSDT",
    "CELOUSDT",
    "CAKEUSDT",
    "FORTHUSDT",
    "ICPUSDT",
    "CLVUSDT",
    "MOVRUSDT",
    "QIUSDT",
    "SPELLUSDT",
    "JOEUSDT",
    "ACAUSDT",
    "GMTUSDT",
    "APEUSDT",
    "APTUSDT",
    "AGIXUSDT",
    "ARKMUSDT",
    "MEMEUSDT",
    "AIUSDT",
    "MANTAUSDT",
    "ALTUSDT",
    "JUPUSDT",
    "PYTHUSDT",
    "PORTALUSDT",
]
SYMBOLS_10M = [
    "NEOUSDT",
    "QTUMUSDT",
    "EOSUSDT",
    "IOTAUSDT",
    "XLMUSDT",
    "ICXUSDT",
    "VETUSDT",
    "HOTUSDT",
    "ZILUSDT",
    "ZECUSDT",
    "IOSTUSDT",
    "CELRUSDT",
    "THETAUSDT",
    "ENJUSDT",
    "ONEUSDT",
    "ANKRUSDT",
    "MTLUSDT",
    "DENTUSDT",
    "CHZUSDT",
    "XTZUSDT",
    "RVNUSDT",
    "STXUSDT",
    "KAVAUSDT",
    "IOTXUSDT",
    "RLCUSDT",
    "CTXCUSDT",
    "TROYUSDT",
    "FTTUSDT",
    "OGNUSDT",
    "DREPUSDT",
    "LSKUSDT",
    "COTIUSDT",
    "CTSIUSDT",
    "CHRUSDT",
    "MDTUSDT",
    "STMXUSDT",
    "LRCUSDT",
    "PNTUSDT",
    "COMPUSDT",
    "SCUSDT",
    "ZENUSDT",
    "SNXUSDT",
    "SXPUSDT",
    "STORJUSDT",
    "MANAUSDT",
    "YFIUSDT",
    "CRVUSDT",
    "OCEANUSDT",
    "LUNAUSDT",
    "RSRUSDT",
    "TRBUSDT",
    "SUSHIUSDT",
    "KSMUSDT",
    "EGLDUSDT",
    "DIAUSDT",
    "UMAUSDT",
    "BELUSDT",
    "WINGUSDT",
    "FLMUSDT",
    "ORNUSDT",
    "XVSUSDT",
    "AAVEUSDT",
    "AUDIOUSDT",
    "AKROUSDT",
    "AXSUSDT",
    "STRAXUSDT",
    "UNFIUSDT",
    "ROSEUSDT",
    "SKLUSDT",
    "1INCHUSDT",
    "CKBUSDT",
    "TWTUSDT",
    "LITUSDT",
    "SFPUSDT",
    "DODOUSDT",
    "OMUSDT",
    "DEGOUSDT",
    "LINAUSDT",
    "PERPUSDT",
    "CFXUSDT",
    "TLMUSDT",
    "BAKEUSDT",
    "BURGERUSDT",
    "SLPUSDT",
    "ARUSDT",
    "MASKUSDT",
    "LPTUSDT",
    "XVGUSDT",
    "GTCUSDT",
    "KLAYUSDT",
    "BONDUSDT",
    "C98USDT",
    "QNTUSDT",
    "FLOWUSDT",
    "MINAUSDT",
    "RAYUSDT",
    "XECUSDT",
    "DYDXUSDT",
    "VIDTUSDT",
    "ILVUSDT",
    "YGGUSDT",
    "FIDAUSDT",
    "FRONTUSDT",
    "RADUSDT",
    "BETAUSDT",
    "AUCTIONUSDT",
    "BNXUSDT",
    "ENSUSDT",
    "KP3RUSDT",
    "POWRUSDT",
    "JASMYUSDT",
    "PYRUSDT",
    "FXSUSDT",
    "HIGHUSDT",
    "PEOPLEUSDT",
    "ACHUSDT",
    "IMXUSDT",
    "GLMRUSDT",
    "API3USDT",
    "WOOUSDT",
    "TUSDT",
    "ASTRUSDT",
    "GALUSDT",
    "LDOUSDT",
    "EPXUSDT",
    "LEVERUSDT",
    "STGUSDT",
    "LUNCUSDT",
    "GMXUSDT",
    "POLYXUSDT",
    "HFTUSDT",
    "PHBUSDT",
    "HOOKUSDT",
    "MAGICUSDT",
    "VIBUSDT",
    "SSVUSDT",
    "AMBUSDT",
    "USTCUSDT",
    "GASUSDT",
    "GLMUSDT",
    "LOOMUSDT",
    "RDNTUSDT",
    "EDUUSDT",
    "MAVUSDT",
    "PENDLEUSDT",
    "CYBERUSDT",
    "GFTUSDT",
    "IQUSDT",
    "NTRNUSDT",
    "BEAMXUSDT",
    "BLURUSDT",
    "JTOUSDT",
    "ACEUSDT",
    "NFPUSDT",
    "XAIUSDT",
    "RONINUSDT",
    "DYMUSDT",
    "PDAUSDT",
    "AXLUSDT",
    "METISUSDT",
]
SYMBOLS_OTHER = [
    "ONTUSDT",
    "NULSUSDT",
    "ONGUSDT",
    "BATUSDT",
    "DASHUSDT",
    "OMGUSDT",
    "TFUELUSDT",
    "DUSKUSDT",
    "WINUSDT",
    "COSUSDT",
    "KEYUSDT",
    "DOCKUSDT",
    "FUNUSDT",
    "CVCUSDT",
    "BANDUSDT",
    "RENUSDT",
    "NKNUSDT",
    "VITEUSDT",
    "WRXUSDT",
    "BNTUSDT",
    "MBLUSDT",
    "STPTUSDT",
    "DATAUSDT",
    "HIVEUSDT",
    "ARDRUSDT",
    "KNCUSDT",
    "VTHOUSDT",
    "DGBUSDT",
    "BALUSDT",
    "BLZUSDT",
    "IRISUSDT",
    "KMDUSDT",
    "JSTUSDT",
    "NMRUSDT",
    "PAXGUSDT",
    "OXTUSDT",
    "SUNUSDT",
    "ALPHAUSDT",
    "CTKUSDT",
    "HARDUSDT",
    "AVAUSDT",
    "XEMUSDT",
    "PSGUSDT",
    "OGUSDT",
    "RIFUSDT",
    "TRUUSDT",
    "BADGERUSDT",
    "FISUSDT",
    "PONDUSDT",
    "ALICEUSDT",
    "SUPERUSDT",
    "TKOUSDT",
    "PUNDIXUSDT",
    "POLSUSDT",
    "MDXUSDT",
    "ATAUSDT",
    "ERNUSDT",
    "PHAUSDT",
    "DEXEUSDT",
    "FARMUSDT",
    "ALPACAUSDT",
    "QUICKUSDT",
    "FORUSDT",
    "REQUSDT",
    "GHSTUSDT",
    "WAXPUSDT",
    "GNOUSDT",
    "ELFUSDT",
    "IDEXUSDT",
    "SYSUSDT",
    "DFUSDT",
    "CVPUSDT",
    "AGLDUSDT",
    "RAREUSDT",
    "LAZIOUSDT",
    "CHESSUSDT",
    "ADXUSDT",
    "DARUSDT",
    "PORTOUSDT",
    "ALCXUSDT",
    "SANTOSUSDT",
    "BICOUSDT",
    "FLUXUSDT",
    "VOXELUSDT",
    "CVXUSDT",
    "LOKAUSDT",
    "SCRTUSDT",
    "BTTCUSDT",
    "XNOUSDT",
    "KDAUSDT",
    "BSWUSDT",
    "STEEMUSDT",
    "MOBUSDT",
    "NEXOUSDT",
    "REIUSDT",
    "OSMOUSDT",
    "RPLUSDT",
    "PROSUSDT",
    "GNSUSDT",
    "SYNUSDT",
    "LQTYUSDT",
    "PROMUSDT",
    "UFTUSDT",
    "OAXUSDT",
    "AERGOUSDT",
    "ASTUSDT",
    "SNTUSDT",
    "COMBOUSDT",
    "WBETHUSDT",
    "ARKUSDT",
    "CREAMUSDT",
    "PIVXUSDT",
    "VICUSDT",
    "AEURUSDT",
]
STABLE_COINS = ["TUSDUSDT", "USDCUSDT", "FDUSDUSDT"]
DONT_USE_SYMBOLS = [
    "PAXGUSDT",  # low amplitude
]

SYMBOLS = SYMBOLS_100M + SYMBOLS_50M + SYMBOLS_10M + SYMBOLS_OTHER

AlligatorTfsTuple = namedtuple("AlligatorTFs", ["fast", "middle", "long", "vlong"])

ValuesMA_ = namedtuple("ValuesMA", ["time", "value", "delta", "state"])


class ValuesMA(ValuesMA_):
    def __repr__(self):
        return f"{self.time} {self.value} {self.delta} {self.state}"


AlligatorValues_ = namedtuple("AlligatorValues", ["name", "lips", "teeth", "jaw"])


class AlligatorValues(AlligatorValues_):
    def __repr__(self):
        return f"{self.name}: \n\t{self.lips} \n\t{self.teeth} \n\t{self.jaw}"


AlligatorValuesPool_ = namedtuple(
    "AlligatorValuesPool", ["symbol", "fast", "middle", "long", "vlong"]
)


class AlligatorValuesPool(AlligatorValuesPool_):
    def __repr__(self):
        return (
            f"{self.symbol}: \n{self.fast} \n{self.middle} \n{self.long} \n{self.vlong}"
        )


# lips, teeth, jaw - MovingAverage Dataframes
AlligatorState_ = namedtuple("AlligatorState", ["name", "lips", "teeth", "jaw"])


class AlligatorState(AlligatorState_):
    def __repr__(self):
        return f"{self.name} {self.lips} {self.teeth} {self.jaw}"


AlligatorStatePool_ = namedtuple(
    "AlligatorStatePool", ["symbol", "fast", "middle", "long", "vlong"]
)


class AlligatorStatePool(AlligatorStatePool_):
    def __repr__(self):
        return (
            f"{self.symbol}: \n{self.fast} \n{self.middle} \n{self.long} \n{self.vlong}"
        )


class StateEnum(Enum):
    FRENZY = 9
    EAGLE = 8
    GENTLE = 7
    BREEZE = 6
    FLAT = 5
    RETREAT = 4
    DECLINE = 3
    CRASH = 2
    PANIC = 1


class EnumAlligatorDirection(Enum):
    UP = 2
    UPCORRECTION = 1
    UNCERTAIN = 0
    DOWNCORRECTION = -1
    DOWN = -2


if __name__ == "__main__":
    print(len(SYMBOLS_10M))
    # =================================================

    # from datetime import date
    # class Weekday(Enum):
    #     MONDAY = 1
    #     TUESDAY = 2
    #     WEDNESDAY = 3
    #     THURSDAY = 4
    #     FRIDAY = 5
    #     SATURDAY = 6
    #     SUNDAY = 7
    #
    #     @classmethod
    #     def today(cls):
    #         print('today is %s' % cls(date.today().isoweekday()).name)
    #
    # for x in Weekday:
    #     print(type(x.value))

    # =================================================

    # interval = Interval(name='15m')
    # print(interval.name)
    # print(interval.ms)
    # print(interval.__repr__())
    # print(interval.__str__())

    # name = 'MIN1'
    # s = IntervalNameEnum.MIN5           # IntervalNameEnum.MIN5
    # s = IntervalNameEnum('5m')          # IntervalNameEnum.MIN5
    # s = IntervalNameEnum.MIN5.name      # MIN5
    # s = IntervalNameEnum('5m').name     # MIN5
    # s = IntervalNameEnum.MIN5.value     # '5m'
    # s = IntervalNameEnum('5m').value    # '5m'
    # print(s)

    # =================================================
    pass
