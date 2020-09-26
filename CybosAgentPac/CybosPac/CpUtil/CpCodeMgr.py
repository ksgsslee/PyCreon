from UtilAgentPac.UtilPac.ClassUtil import Singleton
from UtilAgentPac.UtilPac import EtcUtil as Eu
from Config.DefaultConfig import DefaultConfig as Dc
from Config.CybosAgentConfig import CybosAgentConfig as Cac
import win32com.client
import logging
import pandas as pd


class CpCodeMgr(metaclass=Singleton):
    """
    http://money2.daishin.com/e5/mboard/ptype_basic/HTS_Plus_Helper/DW_Basic_Read_Page.aspx?boardseq=284&seq=11&page=1&searchString=CpCodeMgr&p=8839&v=8642&m=9508
    """
    # # member variable
    support_db_info = {
        'StockInfo': {
            'DataName': ['Id', 'StockName', 'MarketKind', 'SectionKind', 'Kospi200Kind', 'ControlKind',
                         'SupervisionKind', 'StatusKind', 'CapitalSize', 'LacKind', 'ListedDate', 'ParPrice',
                         'MemeMin'],
            'KeyName': 'Id',
            'Type': 'pickle',
        },
        'StockInfoKospiKosdaq': {
            'DataName': ['Id', 'StockName', 'MarketKind', 'SectionKind', 'Kospi200Kind', 'ControlKind',
                         'SupervisionKind', 'StatusKind', 'CapitalSize', 'LacKind', 'ListedDate', 'ParPrice',
                         'MemeMin'],
            'KeyName': 'Id',
            'Type': 'csv'
        }
    }
    support_data_info = {
        'Id': [str],
        'StockName': [str],
        'MarketKind': [str],
        'SectionKind': [str],
        'Kospi200Kind': [str],
        'ControlKind': [str],
        'SupervisionKind': [str],
        'StatusKind': [str],
        'CapitalSize': [str],
        'LacKind': [str],
        'ListedDate': [int],
        'ParPrice': [int],
        'MemeMin': [int],
    }

    # # initialize
    def __init__(self):
        self.obj = win32com.client.Dispatch("CpUtil.CpCodeMgr")

        self.update_db_func = {
            'StockInfo': self._update_stock_info,
        }
        self.update_db_w_all_id_wo_date_func = {
            'StockInfoKospiKosdaq': self._update_stock_info_kospi_kosdaq
        }

        self.log = logging.getLogger('log_all')
        self.log.info("CpUtil.CpCodeMgr Ready")

    # # public function
    def update_db(self, db_name, target_ids):
        """
        update db based on id
        :param db_name: str
        :param target_ids: list
        :return: _
        """
        self.update_db_func[db_name](db_name, target_ids)

    def update_db_w_all_id_wo_date(self, db_name):
        """
        update db with all id without date
        :param db_name: str
        :return: _
        """
        self.update_db_w_all_id_wo_date_func[db_name](db_name)

    def get_id_in_market(self, market):
        """
        get id in market
        :param market: int
        :return: lis
        """
        return self.obj.GetStockListByMarket(market)

    def get_stock_info_kospi_kosdaq(self):
        """
        get stock info kospi kosdaq
        :return: df
        """
        return self._update_stock_info_kospi_kosdaq('StockInfoKospiKosdaq')

    # # protected function
    def _update_stock_info(self, db_name, target_ids):
        """
        update stock info
        :param db_name: str
        :param target_ids: list
        :return: _
        """
        db_type = self.support_db_info[db_name]['Type']

        path_left = Eu.make_dir_return_path(Cac.DbPath + db_name + '/')
        for ele_id in target_ids:
            exist, stock_info_old = Eu.read_df(path_left, ele_id, db_type)
            stock_info_new = self._get_cybos_stock_info(ele_id)

            if exist and stock_info_old.equals(stock_info_new):
                self.log.info(ele_id + ': ' + "StockInfo Update : All Same")
                continue

            Eu.write_df(stock_info_new, path_left, ele_id, db_type)
            self.log.info(ele_id + ': ' + "StockInfo Update : Write")

    def _update_stock_info_kospi_kosdaq(self, db_name):
        """
        update stock info kospi kosdaq
        :param db_name: str
        :return: df
        """
        db_type = self.support_db_info[db_name]['Type']

        target_id_kospi_kosdaq = []
        for market in [1, 2]:
            target_id_kospi_kosdaq += list(self.get_id_in_market(market))
        report_path_left = Cac.ReportPath + db_name + '/'
        db_path_left = Eu.make_dir_return_path(Cac.DbWAllIdWoDatePath + db_name + '/')

        exist, stock_info_old = Eu.read_df(db_path_left, db_name, db_type)
        if stock_info_old is not None:
            d_type = {}
            for column in stock_info_old.columns:
                d_type[column] = self.support_data_info[column][0]
            stock_info_old = stock_info_old.astype(d_type)

        stock_info_new = self._get_cybos_stock_info(target_id_kospi_kosdaq)

        if exist and stock_info_old.equals(stock_info_new):
            self.log.info("stock info kospi kosdaq all same")
            return stock_info_new

        Eu.write_df(stock_info_new, db_path_left, db_name, db_type)

        if not exist:
            self.log.info("stock info kospi kosdaq new write")
            return stock_info_new

        stock_info_new_ori = stock_info_new.copy()
        stock_info_change = {'Id': [], 'StockName': [], 'ChangeType': [], 'Before': [], 'After': []}
        id_in = list(set(list(stock_info_new.Id)) - set(list(stock_info_old.Id)))
        if not len(id_in) == 0:
            self.log.info("1. In (" + str(len(id_in)) + ')')
            mask_index = pd.Series([True] * len(stock_info_new))

            for ele_id in id_in:
                stock_info_in = stock_info_new.loc[stock_info_new.Id == ele_id, :].reset_index(drop=True)
                Eu.append_list_to_dic([ele_id, stock_info_in.loc[0, 'StockName'], 'In', 'None', 'None'],
                                      stock_info_change)

                mask_index = mask_index & (stock_info_new.Id != ele_id)

            stock_info_new = stock_info_new.loc[mask_index, :].reset_index(drop=True)

        id_out = list(set(list(stock_info_old.Id)) - set(list(stock_info_new.Id)))
        if not len(id_out) == 0:
            self.log.info("2. Out (" + str(len(id_out)) + ')')
            mask_index = pd.Series([True] * len(stock_info_old))

            for ele_id in id_out:
                stock_info_out = stock_info_old.loc[stock_info_old.Id == ele_id, :].reset_index(drop=True)
                Eu.append_list_to_dic([ele_id, stock_info_out.loc[0, 'StockName'], 'Out', 'None', 'None'],
                                      stock_info_change)

                mask_index = mask_index & (stock_info_old.Id != ele_id)

            stock_info_old = stock_info_old.loc[mask_index, :].reset_index(drop=True)

        stock_info_new = stock_info_new.sort_values(['Id']).reset_index(drop=True)
        stock_info_old = stock_info_old.sort_values(['Id']).reset_index(drop=True)
        content_change_count = 0
        for index in stock_info_new.index:
            if not stock_info_new.loc[index, ].equals(stock_info_old.loc[index, ]):
                content_change_count = content_change_count + 1

                for column in stock_info_new.columns:
                    if stock_info_new.loc[index, column] != stock_info_old.loc[index, column]:
                        Eu.append_list_to_dic(
                            [stock_info_new.loc[index, 'Id'], stock_info_new.loc[index, 'StockName'], column,
                             stock_info_old.loc[index, column], stock_info_new.loc[index, column]], stock_info_change)

        if content_change_count != 0:
            self.log.info("3. Content (" + str(content_change_count) + ')')

        stock_info_change = pd.DataFrame(stock_info_change)
        Eu.write_df(stock_info_change, report_path_left, str(Dc.TodayDate), 'csv')

        return stock_info_new_ori

    def _get_cybos_stock_info(self, target_id):
        """
        get cybos stock info
        :param target_id: str
        :return: df
        """
        if type(target_id) is not list:
            target_id = [target_id]

        stock_info = {
            'Id': [], 'StockName': [], 'MarketKind': [], 'SectionKind': [], 'Kospi200Kind': [],
            'ControlKind': [], 'SupervisionKind': [], 'StatusKind': [], 'CapitalSize': [], 'LacKind': [],
            'ListedDate': [], 'ParPrice': [], 'MemeMin': []
        }

        for ele_target_id in target_id:
            stock_info['Id'].append(str(ele_target_id))
            stock_info['StockName'].append(str(self.obj.CodeToName(ele_target_id)))
            stock_info['MarketKind'].append(MarketKind[int(self.obj.GetStockMarketKind(ele_target_id))])
            stock_info['SectionKind'].append(SectionKind[int(self.obj.GetStockSectionKind(ele_target_id))])
            stock_info['Kospi200Kind'].append(Kospi200Kind[int(self.obj.GetStockKospi200Kind(ele_target_id))])
            stock_info['ControlKind'].append(ControlKind[int(self.obj.GetStockControlKind(ele_target_id))])
            stock_info['SupervisionKind'].append(SupervisionKind[int(self.obj.GetStockSupervisionKind(ele_target_id))])
            stock_info['StatusKind'].append(StatusKind[int(self.obj.GetStockStatusKind(ele_target_id))])
            stock_info['CapitalSize'].append(CapitalSize[int(self.obj.GetStockCapital(ele_target_id))])
            stock_info['LacKind'].append(LacKind[int(self.obj.GetStockLacKind(ele_target_id))])
            stock_info['ListedDate'].append(int(self.obj.GetStockListedDate(ele_target_id)))
            stock_info['ParPrice'].append(int(self.obj.GetStockParPrice(ele_target_id)))
            stock_info['MemeMin'].append(int(self.obj.GetStockMemeMin(ele_target_id)))

        stock_info = pd.DataFrame(stock_info)

        d_type = {}
        for column in stock_info.columns:
            d_type[column] = self.support_data_info[column][0]
        stock_info = stock_info.astype(d_type)

        return stock_info.reset_index(drop=True)


# # global variable
MarketKind = {
    0: "None",        # nothing
    1: "Kospi",       # kospi
    2: "Kosdaq",      # kosdaq
    3: "FreeBoard",   # outside stock
    4: "Krx"          # Korea rx
}

SectionKind = {
    0: "None",              # nothing
    1: "ST",                # sovereignty
    2: "MF",                # investment company
    3: "RT",                # real estate investment company
    4: "SC",                # ship investment company
    5: "IF",                # social indirect capital investment subsidiary
    6: "DR",                # stock deposit certificate
    7: "SW",                # certificate of acquisition
    8: "SR",                # certificate of acquisition
    9: "ELW",               # elw
    10: "ETF",              # etf
    11: "BC",               # profitable securities
    12: "ForeignETF",       # foreign etr
    13: "Foreign",          # foreign stock
    14: "Future",           # future
    15: "Option",           # option
    16: 'NotExist',         # not exist
    17: 'NotExist',         # not exist
}

ControlKind = {
    0: "Normal",            # normal
    1: "Attention",         # attention
    2: "Warning",           # warning
    3: "DangerNotice",      # danger notice
    4: "Danger",            # danger
}

SupervisionKind = {
    0: "Normal",            # normal
    1: "Supervision",       # in supervision
}

StatusKind = {
    0: "Normal",            # normal
    1: "Stop",              # stop
    2: "Break",             # break (not stop)
}

CapitalSize = {
    0: "None",              # don't care
    1: "Large",             # large
    2: "Middle",            # middle
    3: "Small",             # small
}

Kospi200Kind = {
    0: "None",                          # none
    1: "ConstructionsMachinery",        # construction
    2: "ShipBuildingTransportation",    # transportation
    3: "SteelsMaterials",               # steel
    4: "EnergyChemicals",               # energy
    5: "IT",                            # it
    6: "Finance",                       # finance
    7: "CustomerStaples",               # customer essential goods
    8: "CustomerDiscretionary",         # customer goods
    9: 'NotExist',                      # not exist
    10: 'NotExist',                     # not exist
    11: 'NotExist'                      # not exist
}

LacKind = {
    0: "None",                          # nothing
    1: "ExRights",                      # right lock
    2: "ExDividend",                    # dividend
    3: "ExDistriDividend",              # distribution lock
    4: "ExRightsDividend",              # winding
    5: "InterimDividend",               # medium dividend
    6: "ExRightsInterimDividend",       # right interim dividend
    7: "Etc",                           # etc
}
