from Config.DefaultConfig import DefaultConfigOri as Dco


class DbAgentConfigOri:
    # # frequent changed config
    UpdateDbTargetId = None
    UpdateDbTargetIdCond = [
        ["MarketKind == 'Kosdaq'", "SectionKind == 'ST'", "ListedDate <= 20090101"],
        ["Kospi200Kind != 'None'", "ListedDate <= 20090101"],
        ["SectionKind == 'ETF'", "ListedDate <= 20090101"]
    ]

    # # not frequent changed config
    DbPath = Dco.StoragePath + "Db/"
    DbWAllIdWoDatePath = Dco.StoragePath + 'DbWAllIdWoDate/'

    ReportPath = Dco.ReportPath


# # frequent changed config

# # not frequent changed config

# make instance
DbAgentConfig = DbAgentConfigOri()
