import os
import logging


def make_log(log_path, log_level, log_name):
    """
    make log
    :param log_path: str
    :param log_level: int
    :param log_name: str
    :return: _
    """
    # config
    log_level_info = {
        0: logging.DEBUG,
        1: logging.INFO,
        2: logging.WARNING,
        3: logging.ERROR,
        4: logging.CRITICAL
    }

    if not os.path.exists(log_path):
        os.makedirs(log_path)

    # if exist
    if os.path.exists(log_path + log_name + ".log"):
        os.remove(log_path + log_name + ".log")

    log = logging.getLogger(log_name)
    log.setLevel(log_level_info[log_level])

    formatter = logging.Formatter('[%(levelname)s] (%(filename)s:%(lineno)d) > %(message)s')

    file_handler = logging.FileHandler(log_path + log_name + ".log")
    stream_handler = logging.StreamHandler()

    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    log.addHandler(file_handler)
    log.addHandler(stream_handler)
