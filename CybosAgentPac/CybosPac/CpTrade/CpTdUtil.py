from UtilAgentPac.UtilPac.ClassUtil import Singleton
import win32com.client
import logging


class CpTdUtil(metaclass=Singleton):
    """
    http://money2.daishin.com/e5/mboard/ptype_basic/HTS_Plus_Helper/DW_Basic_Read_Page.aspx?boardseq=284&seq=154&page=1&searchString=CpTdUtil&p=8839&v=8642&m=9508
    """

    def __init__(self):
        self.obj = win32com.client.Dispatch("CCpTrade.CpTdUtil")
        self.log = logging.getLogger('log_all')

        self.log.info("CpTrade.CpTdUtil Ready")

    def get_account_number(self):
        """
        get account number
        :return: int
        """
        return self.obj.AccountNumber

    def get_goods_list(self, acc, goods_filter):
        """
        get goods list
        :param acc: ?
        :param goods_filter: ?
        :return: ?
        """
        return self.obj.GoodsList(acc, goods_filter)

    def trade_init(self):
        """
        trade init
        :return: bool
        """
        return self.obj.TradeInit(0)
