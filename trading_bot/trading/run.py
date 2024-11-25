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
        self.config = Config()
        self.storage = Storage()
        self.trader = Trader(cfg=self.config)
        self.data = DataController(storage=self.storage)
        self.strategist = Strategy(config=self.config, data_ctrl=self.data, trader=self.trader)
        self._th_stop_event = th.Event()

    def run(self):
        self._logger.info("Starting...")
        self.strategist.init_data_ctrl()

        schedule = SafeScheduler(logger)
        schedule.every(self.config.SCOUT_SLEEP_TIME).seconds.do(self.strategist.scout).tag(
            "scouting"
        )

        while True:
            schedule.run_pending()
            time.sleep(1)

    def stop(self):
        self._logger.debug("Stopping all streams...")
        self.strategist.data_ctrl.stop()
        self._th_stop_event.set()

    def account(self):
        return self.trader.account(omitZeroBalance=True)


broker = Broker()
