import pandas as pd
from trading.enums import enums


def streamdata_to_dataframe(data: dict) -> pd.DataFrame:
    """Sample data from kline stream:
              data = {
                        "t": 123400000, // Kline start time
                        "T": 123460000, // Kline close time
                        "s": "BNBBTC",  // Symbol
                        "i": "1m",      // Interval
                        "f": 100,       // First trade ID
                        "L": 200,       // Last trade ID
                        "o": "0.0010",  // Open price
                        "c": "0.0020",  // Close price
                        "h": "0.0025",  // High price
                        "l": "0.0015",  // Low price
                        "v": "1000",    // Base asset volume
                        "n": 100,       // Number of trades
                        "x": false,     // Is this kline closed?
                        "q": "1.0000",  // Quote asset volume
                        "V": "500",     // Taker buy base asset volume
                        "Q": "0.500",   // Taker buy quote asset volume
                        "B": "123456"   // Ignore
                      }

            :param data:
            :return:
            """
    new_data = []
    for value in enums.STREAMKLINE_COLUMNS:
        new_data.append(data[f'{value}'])

    df = pd.DataFrame(
        [new_data],
        columns=enums.COLUMNS.keys(),
        index=[data['t']]
    )
    df = df.astype(enums.COLUMNS, copy=False)

    return df

