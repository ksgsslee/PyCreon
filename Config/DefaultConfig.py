import datetime


class DefaultConfigOri:
    # # frequent changed config
    RootPath = "C:/Users/kwole/Desktop/PyProject/"

    # # not frequent changed config
    ProjectName = 'PyCreon'
    InvalidNum = -999999999
    TodayDate = int(datetime.datetime.now().strftime("%Y%m%d"))
    StoragePath = RootPath + "Storage/"
    ReportPath = RootPath + "Report/"


# # frequent changed config

# # not frequent changed config

# make instance
DefaultConfig = DefaultConfigOri()
