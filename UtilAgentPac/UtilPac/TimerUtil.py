import time


def stamp_start_time():
    """
    stamp start time
    :return: float (sec)
    """
    return time.time()


def get_elapsed_time(start_time):
    """
    get elapsed time
    :param start_time: float
    :return: float
    """
    return time.time() - start_time
