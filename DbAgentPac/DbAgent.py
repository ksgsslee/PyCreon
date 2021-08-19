from UtilAgentPac.UtilPac.ClassUtil import Singleton
from Config.DbAgentConfig import DbAgentConfig as Dac
from CybosAgentPac.CybosAgent import CybosAgent
from UtilAgentPac.UtilPac.EtcUtil import dump_json
import sys
import logging


class DbAgent(metaclass=Singleton):
    # # initialize
    def __init__(self):
        self.log = logging.getLogger('log_all')
        self.log.info('DbAgent Ready')

        self.cybos_agent = CybosAgent()
        self.ids_max_num = 3000

    # # public function
    def update_db(self):
        """
        update db
        :return: _
        """
        update_info = {}

        target_ids = Dac.UpdateDbTargetId
        if target_ids is None:
            target_ids = ['U001', 'U201'] + self.get_ids_with_condition(Dac.UpdateDbTargetIdCond)

        self.log.warning("{} Nummber of Stock wiil be Updated".format(len(target_ids)))

        self.cybos_agent.update_db(update_info, target_ids)

        self._dump_update_db_info(update_info)

    def update_db_w_all_id_wo_date(self):
        """
        update db with all id without date
        :return: _
        """
        update_info = {}

        self.cybos_agent.update_db_w_all_id_wo_date(update_info)

        self._dump_update_db_w_all_id_wo_date_info(update_info)

    def get_ids_with_condition(self, conditions):
        """
        get ids with condition
        :param conditions: list
        :return: list
        """
        class_obj = self.cybos_agent.get_cybos_obj('CpCodeMgr')
        stock_info = class_obj.get_stock_info_kospi_kosdaq()
        # stock_info = stock_info.loc[stock_info['StatusKind'] != 'Stop', :].reset_index(drop=True)

        target_all = None
        for condition_ands in conditions:
            if type(condition_ands) != list:
                self.log.warning('Error'), sys.exit()

            target_sub = None
            for condition in condition_ands:
                target = stock_info.eval(condition)
                target_sub = target if target_sub is None else target_sub & target

            target_all = target_sub if target_all is None else target_all | target_sub

        target_stock_info = stock_info.loc[target_all, :]

        return list(target_stock_info['Id'])[:self.ids_max_num]

    # # protected function
    def _dump_update_db_info(self, update_info):
        """
        dump update db info
        :param update_info: dic
        :return: _
        """
        db_name_all = []
        data_name_all = []
        for key_db_name, val_db_info in update_info.items():
            db_name_all.append(key_db_name)

            if ['DataName', 'KeyName', 'Type'] != list(val_db_info.keys()):
                self.log.warning("Error"), sys.exit(False)

            if val_db_info['KeyName'] not in val_db_info['DataName']:
                self.log.warning("Error"), sys.exit(False)

            data_name = val_db_info['DataName'].copy()
            data_name.remove(val_db_info['KeyName'])
            data_name_all += data_name

        db_name_all_unique = list(set(db_name_all))
        data_name_all_unique = list(set(data_name_all))

        if (db_name_all.sort() != db_name_all_unique.sort()) or\
                (data_name_all.sort() != data_name_all_unique.sort()):
            self.log.warning("Error"), sys.exit(False)

        self.log.info("Dump DbInfo")
        dump_json(update_info, Dac.DbPath, 'DbInfo')

    def _dump_update_db_w_all_id_wo_date_info(self, update_info):
        """
        dump update db w all id without date info
        :param update_info: dic
        :return: _
        """
        db_name_all = []
        for key_db_name, val_db_info in update_info.items():
            db_name_all.append(key_db_name)

        db_name_all_unique = list(set(db_name_all))

        if db_name_all.sort() != db_name_all_unique.sort():
            self.log.warning("Error"), sys.exit(False)

        self.log.info("Dump DbWAllIdWoDateInfo")
        dump_json(update_info, Dac.DbWAllIdWoDatePath, 'DbWAllIdWoDateInfo')
