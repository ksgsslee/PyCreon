from UtilAgentPac.UtilPac.ClassUtil import Singleton
import win32com.client
import logging


class CpCybos(metaclass=Singleton):
    """
    http://money2.daishin.com/e5/mboard/ptype_basic/HTS_Plus_Helper/DW_Basic_Read_Page.aspx?boardseq=284&seq=2&page=1&searchString=CpCybos&p=8839&v=8642&m=9508
    """

    def __init__(self):
        self.obj = win32com.client.Dispatch("CpUtil.CpCybos")
        self.log = logging.getLogger('log_all')

        self.log.info("CpUtil.Cpcybos Ready")

    def get_is_connect(self):
        """
        get is connected
        :return: int
        """
        return self.obj.IsConnect

    def get_server_type(self):
        """
        get server type
        :return: int
        """
        return self.obj.ServerType

    def get_limit_request_remain_time(self):
        """
        get limit request remain time
        :return: float
        """
        return self.obj.LimitRequestRemainTime

    def get_limit_remain_count(self, limit_type):
        """
        get limit remain count
        :param limit_type: int
        :return:
        """
        return self.obj.GetLimitRemainCount(limit_type)
