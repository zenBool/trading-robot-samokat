import configparser

# Создаем объект ConfigParser
config = configparser.ConfigParser()

# Читаем конфигурационный файл
config.read('trader.cfg')

binance_config = dict(config.items("binance"))

strategy_config = dict(config.items("strategy"))

strategy_triple_screen_config = dict(config.items("strategy-triple-screen"))
