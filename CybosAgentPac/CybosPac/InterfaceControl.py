from UtilAgentPac.UtilPac.ClassUtil import Singleton
from CybosAgentPac.CybosPac.CpUtil.CpCybos import CpCybos
from time import sleep
import logging
import sys


class InterfaceControl(metaclass=Singleton):
    def __init__(self):
        self.log = logging.getLogger('log_all')
        self.log.info("InterfaceControl Ready")

        self.cp_cybos = CpCybos()
        self.mode_to_int = {'Order': 0, 'DB': 1}

    def wait_request_limit(self, mode):
        """
        wait request limit
        :param mode: str ('Order' or 'DB')
        :return: bool
        """
        remain_count = self.cp_cybos.get_limit_remain_count(self.mode_to_int[mode])

        if remain_count > 0:
            return True

        remain_time = self.cp_cybos.get_limit_request_remain_time()
        self.log.info("cybos restriction time wait %.2f sec" % ((remain_time + 500) / 1000.0))
        sleep((remain_time + 500) / 1000)

        return True

    def block_request(self, obj, mode):
        """
        block request
        :param obj: obj
        :param mode: str ('Order' or 'DB')
        :return: bool
        """
        self.wait_request_limit(mode)

        obj.BlockRequest()

        # fail check
        if obj.GetDibStatus() != 0:
            self.log.warning("Error"), sys.exit(False)

        return True

    @staticmethod
    def set_input_value(obj, input_value):
        """
        set input value
        :param obj: obj
        :param input_value: dic
        :return: bool
        """
        for key, value in input_value.items():
            if value is not None:
                obj.SetInputValue(key, value)

        return True
