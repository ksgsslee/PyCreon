from CybosAgentPac.CybosPac.CpUtil import CpCodeMgr
from CybosAgentPac.CybosPac.CpSysDib import StockChart
from CybosAgentPac.CybosPac.CpSysDib import CpSvr7254
from Config.CybosAgentConfig import CybosAgentConfig as Cac
import logging
import sys


class CybosAgentWrapper:
    # # initialize
    def __init__(self):
        self.log = logging.getLogger('log_all')
        self.log.info('CybosAgent Ready')

        self.support_cybos_class = {
            'CpCodeMgr':  CpCodeMgr.CpCodeMgr,
            'StockChart': StockChart.StockChart,
            'CpSvr7254': CpSvr7254.CpSvr7254
        }
        self.support_db_info = {}
        self.support_db_wo_id_info = {}
        self.save_cybos_obj = {}

        self._prepare_support_db_info()
        self._prepare_support_db_wo_id_info()

    # # public function
    def get_cybos_obj(self, class_name):
        """
        get cybos object
        :param class_name: str
        :return inst
        """
        if class_name not in self.support_cybos_class.keys():
            self.log.warning("Error"), sys.exit(False)

        if class_name in self.save_cybos_obj.keys():
            cybos_obj = self.save_cybos_obj[class_name]
        else:
            cybos_obj = self.support_cybos_class[class_name]()
            self.save_cybos_obj[class_name] = cybos_obj

        return cybos_obj

    # # protected function
    def _prepare_support_db_info(self):
        """
        prepare support db info
        :return:
        """
        support_db_name = []

        for class_name in Cac.SupportCybosClassForDb:
            class_obj = self.get_cybos_obj(class_name)

            for db_name in class_obj.support_db_info.keys():
                support_db_name.append(db_name)
                self.support_db_info[db_name] = class_name

        support_db_name_unique = list(set(support_db_name))
        if len(support_db_name_unique) != len(support_db_name):
            self.log.warning("Error"), sys.exit(False)

    def _prepare_support_db_wo_id_info(self):
        """
        prepare support db wo id info
        :return:
        """
        support_db_name = []

        for class_name in Cac.SupportCybosClassForDbWoId:
            class_obj = self.get_cybos_obj(class_name)

            for db_name in class_obj.support_db_info.keys():
                support_db_name.append(db_name)
                self.support_db_wo_id_info[db_name] = class_name

        support_db_name_unique = list(set(support_db_name))
        if len(support_db_name_unique) != len(support_db_name):
            self.log.warning("Error"), sys.exit(False)
