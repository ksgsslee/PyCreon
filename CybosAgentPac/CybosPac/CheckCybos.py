from CybosAgentPac.CybosPac.CpUtil.CpCybos import CpCybos
from CybosAgentPac.CybosPac.CpTrade.CpTdUtil import CpTdUtil
import ctypes
import logging


def check_cybos_mode(mode):
    """
    check cybos mode
    :param mode: str ('Order' or 'DB')
    :return: bool
    """
    log = logging.getLogger('log_all')
    okay = True

    okay &= cybos_connected_check(log)
    okay &= cybos_supervision_mode_check(log)
    if mode == 'Order':
        okay &= cybos_trade_initialize_check(log)

    return okay


def cybos_connected_check(log):
    """
    cybos connected check
    :param log: obj
    :return: bool
    """
    if CpCybos().get_is_connect() == 0:
        log.info("Cybos Not Connected")
        return False

    return True


def cybos_supervision_mode_check(log):
    """
    cybos supervision mode check
    :param log: obj
    :return: bool
    """
    if not ctypes.windll.shell32.IsUserAnAdmin():
        log.info('executed with ordinary permission')
        return False

    return True


def cybos_trade_initialize_check(log):
    """
    cybos trade initialize check
    :param log:
    :return: bool
    """
    if CpTdUtil().trade_init() != 0:
        log.info("trade initialize fail")
        return False

    return True
