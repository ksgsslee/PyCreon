from Config.DefaultConfig import DefaultConfigOri as Dco
from Config.DbAgentConfig import DbAgentConfigOri as Daco


class CybosAgentConfigOri:
    # # frequent changed config
    # update df name
    # UpdateDbName = ['StockInfo', 'StockChart1', 'StockChart2', 'GeoLaeType']
    UpdateDbName = ['StockInfo', 'StockChart1', 'StockChart2']
    UpdateDbWoIdName = ['StockInfoKospiKosdaq']
    SupportCybosClassForDb = ['CpCodeMgr', 'StockChart', 'CpSvr7254']
    SupportCybosClassForDbWoId = ['CpCodeMgr']

    # # not frequent changed config
    DbStartDate = 20090101
    DbPath = Daco.DbPath
    DbWAllIdWoDatePath = Daco.DbWAllIdWoDatePath
    ReportPath = Dco.ReportPath


# # frequent changed config

# # not frequent changed config

# make instance
CybosAgentConfig = CybosAgentConfigOri()
