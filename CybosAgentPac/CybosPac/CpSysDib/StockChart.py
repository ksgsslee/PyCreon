from CybosAgentPac.CybosPac.CpSysDib.CpSysDibWrapper import CpSysDibWrapper
from UtilAgentPac.UtilPac.ClassUtil import Singleton
from Config.CybosAgentConfig import CybosAgentConfig as Cac
from Config.DefaultConfig import DefaultConfig as Dc
from UtilAgentPac.UtilPac import EtcUtil as Eu
import numpy as np
import pandas as pd
import sys


class StockChart(CpSysDibWrapper, metaclass=Singleton):
    """
    http://money2.daishin.com/e5/mboard/ptype_basic/HTS_Plus_Helper/DW_Basic_Read_Page.aspx?boardseq=284&seq=102&page=1&searchString=chart&p=8839&v=8642&m=9508
    """

    # # member variable
    class_name = 'StockChart'
    support_db_info = {
        'StockChart1': {
            'DataName': ['Date', 'SiGa', 'GoGa', 'JeoGa', 'JongGa', 'GeoLaeLyang'],
            'KeyName': 'Date',
            'Type': 'pickle',
        },
        'StockChart2': {
            'DataName': ['Date', 'GeoLaeDaeGeum', 'NuJeogCheGyeolMaeDoSuLyang', 'NuJeogCheGyeolMaeSuSuLyang',
                         'SangJangJuSigSu', 'SiGaChongAeg'],
            'KeyName': 'Date',
            'Type': 'pickle'
        },
        'StockChart3': {
            'DataName': ['Date', 'OeGugInJuMunHanDoSuLyang', 'OeGugInJuMunGaNeungSuLyang', 'OeGugInHyeonBoYuSuLyang',
                         'OeGugInHyeonBoYuBiYul', 'GiGwanSunMaeSu', 'GiGwanNuJeogSunMaeSu'],
            'KeyName': 'Date',
            'Type': 'pickle'
        }
    }
    support_data_info = {
        'Date': [0, 'A', int],
        'SiGa': [2, 'A', int],
        'GoGa': [3, 'A', int],
        'JeoGa': [4, 'A', int],
        'JongGa': [5, 'A', int],
        'GeoLaeLyang': [8, 'A', int],
        'GeoLaeDaeGeum': [9, 'A', np.int64],
        'NuJeogCheGyeolMaeDoSuLyang': [10, 'A', np.int64],
        'NuJeogCheGyeolMaeSuSuLyang': [11, 'A', np.int64],
        'SangJangJuSigSu': [12, 'A', np.int64],
        'SiGaChongAeg': [13, 'A', np.int64],
        'OeGugInJuMunHanDoSuLyang': [14, 'A', int],
        'OeGugInJuMunGaNeungSuLyang': [15, 'A', int],
        'OeGugInHyeonBoYuSuLyang': [16, 'A', int],
        'OeGugInHyeonBoYuBiYul': [17, 'A', float],
        'GiGwanSunMaeSu': [20, 'A', int],
        'GiGwanNuJeogSunMaeSu': [21, 'A', int],
    }
    input_value_type = {
        'A': {1: ord('1'), 6: ord('D'), 9: ord('1')}
    }

    # # initialize
    def __init__(self):
        super().__init__()
        self.update_db_func = {
            'StockChart1': self._update_db,
            'StockChart2': self._update_db,
            'StockChart3': self._update_db
        }
        self.update_db_w_all_id_wo_date_func = {
        }

    # # protected function
    def _get_cybos_db(self, target_id, db_name, start_date=Cac.DbStartDate):
        """
        cybos request
        :param target_id: str
        :param db_name: str
        :param start_date: int
        :return: df
        """
        db_info = self.support_db_info[db_name]
        data_names = db_info['DataName']
        key_name = db_info['KeyName']

        input_value_type = self.support_data_info[data_names[0]][1]
        for ele_data_name in data_names:
            if input_value_type != self.support_data_info[ele_data_name][1]:
                self.log.warning("Error"), sys.exit(False)
        input_value = dict(self.input_value_type[input_value_type])

        if key_name not in data_names:
            self.log.warning("Error"), sys.exit(False)

        data_codes = {}
        for ele_data_name in data_names:
            data_codes[self.support_data_info[ele_data_name][0]] = ele_data_name
        sorted_data_codes = sorted(data_codes.items())

        input_value[5] = []
        cybos_db = {}
        for key_data_code, val_data_name in sorted_data_codes:
            input_value[5].append(key_data_code)
            cybos_db[val_data_name] = []

        if start_date > Dc.TodayDate:
            return pd.DataFrame(cybos_db)

        input_value[0] = target_id
        input_value[2] = int(Dc.TodayDate)
        input_value[3] = int(start_date)

        if not self.interface_control.set_input_value(self.obj, input_value):
            self.log.warning("Error"), sys.exit()

        while True:
            self.interface_control.wait_request_limit('DB')

            if not self.interface_control.block_request(self.obj, 'DB'):
                self.log.warning("Error"), sys.exit()

            row_count = self.obj.GetHeaderValue(3)

            for row_index in range(row_count):
                for column_index, column in enumerate(cybos_db.keys()):
                    cybos_db[column].append(self.obj.GetDataValue(column_index, row_index))

            if not self.obj.Continue:
                break

        cybos_db = pd.DataFrame(cybos_db)
        if (db_name == 'StockChart1') and (target_id in ['U001', 'U201']):
            cybos_db['GeoLaeLyang'] = round(cybos_db['GeoLaeLyang'] / 1000, 0).astype(int)

        d_type = {}
        for column in cybos_db.columns:
            d_type[column] = self.support_data_info[column][2]
        cybos_db = cybos_db.astype(d_type)

        return cybos_db.drop_duplicates(['Date']).sort_values(['Date']).reset_index(drop=True)
