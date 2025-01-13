import pandas as pd
import numpy as np

# Создаем тестовые данные для 15-минутного интервала
dates_15m = pd.date_range(start='2023-01-01', periods=80, freq='15min')
df_15m = pd.DataFrame({
    'time_open': dates_15m,
    'close': np.random.rand(80) * 100,
    'volume': np.random.rand(80) * 1000,
    'ma_5': np.random.rand(80) * 100,
    'ma_13': np.random.rand(80) * 100,
    'ma_34': np.random.rand(80) * 100
})

# Создаем тестовые данные для 1-часового интервала
dates_1h = pd.date_range(start='2023-01-01', periods=20, freq='1h')
df_1h = pd.DataFrame({
    'time_open': dates_1h,
    'h1_close': np.random.rand(20) * 100,
    'h1_volume': np.random.rand(20) * 1000,
    'h1_ma_5': np.random.rand(20) * 100,
    'h1_ma_13': np.random.rand(20) * 100,
    'h1_ma_34': np.random.rand(20) * 100
})

# Создаем тестовые данные для 4-часового интервала
dates_4h = pd.date_range(start='2023-01-01', periods=5, freq='4h')
df_4h = pd.DataFrame({
    'time_open': dates_4h,
    'h4_close': np.random.rand(5) * 100,
    'h4_volume': np.random.rand(5) * 1000,
    'h4_ma_5': np.random.rand(5) * 100,
    'h4_ma_13': np.random.rand(5) * 100,
    'h4_ma_34': np.random.rand(5) * 100
})

# Выводим исходные данные
print("15-минутные данные:")
print(df_15m)
print("\n1-часовые данные:")
print(df_1h)
print("\n4-часовые данные:")
print(df_4h)

# Выполняем слияние с помощью merge
df_merged = pd.merge(df_15m, df_1h, on='time_open', how='left')
df_merged = pd.merge(df_merged, df_4h, on='time_open', how='left')


# Функция для расчета EMA
def EMA(close, previous_ma, period):
    k = 2 / (period + 1)
    return close * k + previous_ma * (1 - k)


# Функция для заполнения NaN значений
def fill_nan_ema(df, column, period, timeframe):
    previous_ma = df[column].first_valid_index()
    previous_ma = df.loc[previous_ma, column]

    for index, row in df.iterrows():
        if pd.isna(row[column]):
            if timeframe == '1h':
                period_start = row['time_open'].replace(minute=0, second=0, microsecond=0)
            elif timeframe == '4h':
                period_start = row['time_open'].replace(hour=row['time_open'].hour - row['time_open'].hour % 4,
                                                        minute=0, second=0, microsecond=0)
            period_start_index = df.index[df['time_open'] == period_start][0]
            previous_ma = df.loc[period_start_index, column]
            df.at[index, column] = EMA(row['close'], previous_ma, period)

    return df


# Заполняем NaN значения для каждого столбца
lips, teeth, jaw = 5, 13, 34
df_merged = fill_nan_ema(df_merged, 'h1_ma_5', lips, '1h')
df_merged = fill_nan_ema(df_merged, 'h1_ma_13', teeth, '1h')
df_merged = fill_nan_ema(df_merged, 'h1_ma_34', jaw, '1h')
df_merged = fill_nan_ema(df_merged, 'h4_ma_5', lips, '4h')
df_merged = fill_nan_ema(df_merged, 'h4_ma_13', teeth, '4h')
df_merged = fill_nan_ema(df_merged, 'h4_ma_34', jaw, '4h')

# Выводим результат слияния и заполнения
# print("\nРезультат слияния и заполнения:")
# print(df_merged.head(20))

# Сохраняем результат в Excel файл
excel_file_path = '~/Downloads/merged_data.xlsx'
df_merged.to_excel(excel_file_path, index=False, engine='openpyxl')
print(f"\nДанные сохранены в файл: {excel_file_path}")