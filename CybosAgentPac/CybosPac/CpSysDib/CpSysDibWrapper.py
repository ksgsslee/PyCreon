from UtilAgentPac.UtilPac import EtcUtil as Eu
from CybosAgentPac.CybosPac.InterfaceControl import InterfaceControl
from Config.CybosAgentConfig import CybosAgentConfig as Cac
import win32com.client
import pandas as pd
import logging
import sys


class CpSysDibWrapper:
    """
    Ref Path
    """
    # # member variable
    class_name = ''
    support_db_info = {}
    support_data_info = {}
    input_value_type = {}

    # # initialize
    def __init__(self):
        self.obj_name = 'CpSysDib.' + self.class_name

        self.obj = win32com.client.Dispatch(self.obj_name)
        self.interface_control = InterfaceControl()

        self.update_db_func = {}
        self.update_db_w_all_id_wo_date_func = {}

        self.log = logging.getLogger('log_all')
        self.log.info(self.obj_name + ' Ready')

    # # public Function
    def update_db(self, db_name, target_id):
        """
        update db
        :param db_name: str
        :param target_id: list of str
        :return: _
        """
        self.update_db_func[db_name](db_name, target_id)

    def update_db_w_all_id_wo_date(self, db_name):
        """
        update db with all id without date
        :param db_name: str
        :return: _
        """
        self.update_db_w_all_id_wo_date[db_name](db_name)

    # # protected function
    def _update_db(self, db_name, target_ids):
        """
        update db
        :param db_name: str
        :param target_ids: list of str
        :return: _
        """
        db_type = self.support_db_info[db_name]['Type']

        path_left = Eu.make_dir_return_path(Cac.DbPath + db_name + '/')
        for ele_id in target_ids:
            exist, old_db = Eu.read_df(path_left, ele_id, db_type)
            new_db = self._get_new_db(ele_id, db_name, old_db)

            if exist and old_db.equals(new_db):
                self.log.info(ele_id + ': ' + db_name + " update : All Same")
                continue

            self.log.info(ele_id + ': ' + db_name + " update : Write")
            Eu.write_df(new_db, path_left, ele_id, db_type)

    def _get_new_db(self, target_id, db_name, old_db):
        """
        get new db
        :param target_id: str
        :param db_name: str
        :param old_db: df
        :return: df
        """
        data_names = self.support_db_info[db_name]['DataName']

        if old_db is None:
            start_date = Cac.DbStartDate
        else:
            if list(old_db.columns) != data_names:
                self.log.warning("Error"), sys.exit(False)

            if old_db['Date'].min() < Cac.DbStartDate:
                start_date = Cac.DbStartDate
            else:
                start_date = old_db['Date'].max()

        cybos_db = self._get_cybos_db(target_id, db_name, start_date)

        if old_db is None:
            new_db = cybos_db
        else:
            new_db = pd.concat([old_db, cybos_db]).drop_duplicates(['Date'])

        return new_db.sort_values(['Date']).reset_index(drop=True)

    def _get_cybos_db(self, target_id, db_name, start_date=Cac.DbStartDate):
        """
        get cybos db
        :param target_id: str
        :param db_name: str
        :param start_date: int
        :return:  df
        """
        return None
