from UtilAgentPac.UtilPac.ClassUtil import Singleton
from CybosAgentPac.CybosUtilPac.CybosAgentWrapper import CybosAgentWrapper
from CybosAgentPac.CybosPac import CheckCybos
from Config.CybosAgentConfig import CybosAgentConfig as Cac
import sys


class CybosAgent(CybosAgentWrapper, metaclass=Singleton):
    # # initialize
    def __init__(self):
        super().__init__()

    # # public function
    def update_db(self, update_info, target_ids, update_db_names=Cac.UpdateDbName):
        """
        update db
        :param update_info:
        :param target_ids: str
        :param update_db_names: list of str
        :return:
        """
        if not CheckCybos.check_cybos_mode('DB'):
            self.log.warning("Error"), sys.exit(False)

        for db_name in update_db_names:
            class_name = self.support_db_info[db_name]
            class_obj = self.get_cybos_obj(class_name)

            self._update_update_db_info(class_obj, db_name, update_info)
            class_obj.update_db(db_name, target_ids)

    def update_db_w_all_id_wo_date(self, update_info, update_db_names=Cac.UpdateDbWoIdName):
        """
        update db with all id without date
        :param update_info: dic
        :param update_db_names: list of str
        :return:
        """
        if not CheckCybos.check_cybos_mode('DB'):
            self.log.warning("Error"), sys.exit(False)

        for db_name in update_db_names:
            class_name = self.support_db_wo_id_info[db_name]
            class_obj = self.get_cybos_obj(class_name)

            self._update_update_db_w_all_id_wo_date_info(class_obj, db_name, update_info)
            class_obj.update_db_w_all_id_wo_date(db_name)

    # # protected function
    def _update_update_db_info(self, class_obj, db_name, update_info):
        """
        update update df info
        :param class_obj: obj
        :param db_name: str
        :param update_info: dic
        :return: _
        """
        if db_name not in class_obj.support_db_info.keys():
            self.log.warning("Error"), sys.exit(False)

        if db_name in update_info.keys():
            self.log.warning("Error"), sys.exit(False)

        db_info = class_obj.support_db_info[db_name]
        if ['DataName', 'KeyName', 'Type'] != list(db_info.keys()):
            self.log.warning("Error"), sys.exit(False)

        if db_info['KeyName'] not in db_info['DataName']:
            self.log.warning("Error"), sys.exit(False)

        update_info[db_name] = db_info

    def _update_update_db_w_all_id_wo_date_info(self, class_obj, db_name, update_info):
        """
        update update db w all id wo date info
        :param class_obj: obj
        :param db_name: str
        :param update_info: dic
        :return: _
        """
        self._update_update_db_info(class_obj, db_name, update_info)
