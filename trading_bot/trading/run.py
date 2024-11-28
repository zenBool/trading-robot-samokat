# trader/run.py
import time
import threading as th
from common.logger import logger

from trading.core.config import Config
from trading.core.storage import Storage
from trading.core.data_controller import DataController
from trading.core.safe_scheduler import SafeScheduler
from trading.core.trader import Trader
from trading.strategies.tripple_screen_strategy import Strategy


class Broker(th.Thread):
    def __init__(self):
        super().__init__()
        self._logger = logger
        self._logger.debug("Start create Broker...")
        self._logger.debug(f"Active threads at start: name: {th.current_thread().getName()}, threads: {th.active_count()}")
        self.config = Config()
        self.storage = Storage()
        self.trader = Trader(cfg=self.config)
        self.data = DataController(storage=self.storage)
        self.strategist = Strategy(config=self.config, data_ctrl=self.data, trader=self.trader)
        self._flag_stop = False
        self._th_stop_event = th.Event()
        self._logger.debug("End create Broker...")
        self._logger.debug(f"Active threads is name: {th.current_thread().getName()} at end_create : {th.active_count()}")

    def run(self):
        self._logger.info("Starting...")
        self._logger.debug(f"RUN Broker... {th.current_thread().getName()}")
        print(f"RUN Broker... {th.current_thread().getName()}")
        self._logger.debug(f"Active threads at start Broker.run() : {th.active_count()}")
        self.strategist.init_data_ctrl()

        schedule = SafeScheduler(logger)
        schedule.every(self.config.SCOUT_SLEEP_TIME).seconds.do(self.strategist.scout).tag(
            "scouting"
        )

        while not self._flag_stop:
            schedule.run_pending()
            self._logger.debug(f"{th.active_count()} active threads")
            self._logger.debug(f"{th.current_thread().getName()}")
            time.sleep(2)

    def stop(self):
        self._logger.debug("Stopping all streams...")
        self._flag_stop = True
        self.strategist.data_ctrl.stop()
        self._th_stop_event.set()

    def account(self):
        return self.trader.account()  # omitZeroBalance=True


broker = Broker()
