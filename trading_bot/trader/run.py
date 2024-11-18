# trader/run.py
from common._logger import logging
import time
import threading


class Run:
    def __init__(self):
        self.is_running = False

    def start_trading(self):
        self.is_running = True
        threading.Thread(
            target=self._trading_loop,
            daemon=True,
        ).start()

    def stop_trading(self):
        self.is_running = False

    def _trading_loop(self):
        while self.is_running:
            # Ваша логика открытия и закрытия сделок

            th = threading.current_thread().name
            print("Trader is working...", th, time.time())
            logging.info("Trader is working... %r", th)

            time.sleep(5)  # Задержка, чтобы симулировать выполнение работы


class Trader(threading.Thread):
    def __init__(self):
        super().__init__()
        self.config = Config()
        self.storage = Storage()
        self.data = DataController(storage=self.storage)
        self.strategist = Strategy(config=self.config, data_ctrl=self.data)
        logging.info("Starting...")
        strategist.init_data_ctrl()

        schedule = SafeScheduler(logger)
        schedule.every(cfg.SCOUT_SLEEP_TIME).seconds.do(strategist.scout).tag("scouting")

    while True:
        schedule.run_pending()
        time.sleep(1)

    except KeyboardInterrupt:
        pass
    finally:
        # stop all streams
        strategist.data_ctrl.stop()


trader = Trader()