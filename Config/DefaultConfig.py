import datetime
from pykrx import stock


class DefaultConfigOri:
    # # frequent changed config
    RootPath = "C:/Users/kwole/Desktop/PyProject/"

    # # not frequent changed config
    ProjectName = 'PyCreon'
    InvalidNum = -999999999
    TodayDate = int(datetime.datetime.now().strftime("%Y%m%d"))
    StoragePath = RootPath + "Storage/"
    ReportPath = RootPath + "Report/"
    CriUpdateRecentDealingDateHour = 18

    def __init__(self):
        self._init_execute_nearest_dealing_date()

    # # protected function
    def _init_execute_nearest_dealing_date(self, manual_dealing_date=None):
        """
        init execute nearest dealing date
        :param manual_dealing_date: int
        :return: _
        """
        if manual_dealing_date is None:
            execute_time = datetime.datetime.now()

            one_month_ago_date = (execute_time - datetime.timedelta(weeks=4)).strftime("%Y%m%d")
            execute_hour = int(execute_time.strftime("%H"))

            cri_dealing = stock.get_market_ohlcv_by_date(one_month_ago_date, str(self.TodayDate), "005930")
            recent_dealing_date = int(cri_dealing.index[len(cri_dealing)-1].strftime("%Y%m%d"))

            if (self.TodayDate == recent_dealing_date) and (execute_hour < self.CriUpdateRecentDealingDateHour):
                recent_dealing_date = cri_dealing.index[len(cri_dealing)-2].strftime("%Y%m%d")
            print('Recent Dealing Date : ' + str(recent_dealing_date))

        else:
            recent_dealing_date = manual_dealing_date
            print('Manual Recent Dealing Date : ' + str(recent_dealing_date))

        self.ExecuteNearestDealingDate = int(recent_dealing_date)


# # frequent changed config

# # not frequent changed config

# make instance
DefaultConfig = DefaultConfigOri()
