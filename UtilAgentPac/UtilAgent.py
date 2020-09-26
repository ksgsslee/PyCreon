from UtilAgentPac.UtilPac import *
from Config.UtilAgentConfig import UtilAgentConfig as Uc
import logging


class UtilAgent(metaclass=ClassUtil.Singleton):
    # # Initialize
    def __init__(self):
        self.log = None

        self._start_project()

    # # public function

    # # protect function
    def _start_project(self):
        for key_log, lis_log in Uc.CreateLogList.items():
            LogUtil.make_log(lis_log[1], lis_log[0], key_log)

        self.log = logging.getLogger('log_all')
        self.log.info("UtilAgent Ready")
