from CybosAgentPac.CybosPac.CpSysDib.CpSysDibWrapper import CpSysDibWrapper
from Config.CybosAgentConfig import CybosAgentConfig as Cac
from Config.DefaultConfig import DefaultConfig as Dc
from UtilAgentPac.UtilPac.ClassUtil import Singleton
import pandas as pd
import sys


class CpSvr7254(CpSysDibWrapper, metaclass=Singleton):
    """
    http://money2.daishin.com/e5/mboard/ptype_basic/HTS_Plus_Helper/DW_Basic_Read_Page.aspx?boardseq=284&seq=242&page=1&searchString=CpSvr7254&p=8839&v=8642&m=9508
    """

    # # member variable
    class_name = 'CpSvr7254'
    support_db_info = {
        'GeoLaeType': {
            'DataName': ['Date', 'GaeIn', 'OeGugIn', 'GiGwanGye', 'GeumYungTuJa', 'BoHeom', 'TuSin', 'EunHaeng',
                         'GiTaGeumYung', 'YeonGiGeum', 'GiTaBeobIn', 'GiTaOeIn', 'SaMoPeonDeu', 'GugGaJiJaChe'],
            'KeyName': 'Date',
            'Type': 'pickle',
        },
    }
    support_data_info = {
        'Date': [0, 'A', int],
        'GaeIn': [1, 'A', int],
        'OeGugIn': [2, 'A', int],
        'GiGwanGye': [3, 'A', int],
        'GeumYungTuJa': [4, 'A', int],
        'BoHeom': [5, 'A', int],
        'TuSin': [6, 'A', int],
        'EunHaeng': [7, 'A', int],
        'GiTaGeumYung': [8, 'A', int],
        'YeonGiGeum': [9, 'A', int],
        'GiTaBeobIn': [10, 'A', int],
        'GiTaOeIn': [11, 'A', int],
        'SaMoPeonDeu': [12, 'A', int],
        'GugGaJiJaChe': [13, 'A', int],
    }
    input_value_type = {
        'A': {1: 6, 4: ord('0'), 5: 0, 6: ord('1')},
    }

    # # initialize
    def __init__(self):
        super().__init__()
        self.update_db_func = {
            'GeoLaeType': self._update_db,
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

        cybos_db = {}
        for key_data_code, val_data_name in sorted_data_codes:
            cybos_db[val_data_name] = []

        if start_date > Dc.TodayDate:
            return pd.DataFrame(cybos_db)

        input_value[0] = target_id

        if not self.interface_control.set_input_value(self.obj, input_value):
            self.log.warning("Error"), sys.exit()

        while True:
            self.interface_control.wait_request_limit('DB')

            if not self.interface_control.block_request(self.obj, 'DB'):
                self.log.warning("Error"), sys.exit()

            row_count = self.obj.GetHeaderValue(1)

            for row_index in range(row_count):
                for column_index, column in enumerate(cybos_db.keys()):
                    cybos_db[column].append(self.obj.GetDataValue(column_index, row_index))

            if min(cybos_db[key_name]) < start_date:
                break

            if not self.obj.Continue:
                break

        cybos_db = pd.DataFrame(cybos_db)
        cybos_db = cybos_db.loc[(cybos_db[key_name] >= start_date) & (cybos_db[key_name] <= Dc.TodayDate), :]\
            .reset_index(drop=True)

        d_type = {}
        for column in cybos_db.columns:
            d_type[column] = self.support_data_info[column][2]
        cybos_db = cybos_db.astype(d_type)

        return cybos_db.drop_duplicates([key_name]).sort_values([key_name]).reset_index(drop=True)
