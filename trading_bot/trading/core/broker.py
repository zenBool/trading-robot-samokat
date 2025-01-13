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

        self._logger.debug(f"Active threads at start: name: {th.current_thread().getName()}, threads: {th.active_count()}")

        self.config = Config()
        self.storage = Storage()
        self.trader = Trader(cfg=self.config)
        self.data = DataController(storage=self.storage)
        self.strategist = Strategy(config=self.config, data_ctrl=self.data, trader=self.trader)
        self._is_running = False
        self._th_stop_event = th.Event()

        self._logger.debug(f"Active threads at END is name: {th.current_thread().getName()} at end_create : {th.active_count()}")

    def start(self):
        if not self._is_running:
            self._is_running = True
            super().start()
        else:
            self._logger.info("Broker is already running.")

    def run(self):
        self._logger.info("Starting...")
        self.strategist.init_data_ctrl()

        schedule = SafeScheduler(logger)
        schedule.every(self.config.SCOUT_SLEEP_TIME).seconds.do(self.strategist.scout).tag(
            "scouting"
        )

        while self._is_running:
            schedule.run_pending()
            time.sleep(2)

    def stop(self):
        self._is_running = False
        self.strategist.data_ctrl.stop()
        self._th_stop_event.set()
        self._logger.info("Stop all streams...")

    def account(self, asset):
        return self.trader.account.asset(asset="USDT")
