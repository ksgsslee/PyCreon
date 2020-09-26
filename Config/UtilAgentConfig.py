from Config.DefaultConfig import DefaultConfigOri as Dco


class UtilAgentConfigOri:
    # # frequent changed config

    # # not frequent changed config
    # log name: [log level, log path]
    CreateLogList = {
        'log_all': [1, Dco.RootPath + Dco.ProjectName + "/Log/"]
    }


# # frequent changed config

# # not frequent changed config

# make instance
UtilAgentConfig = UtilAgentConfigOri()
