import sys
import os
import json
import pandas as pd


def make_dir_return_path(dir_path):
    """
    make directory & return path
    :param dir_path: str
    :return: str
    """
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    return dir_path


def print_progress(iteration, total, prefix='', suffix='', decimals=1, bar_length=100):
    """
    print progress
    :param iteration: int or float
    :param total: int or float
    :param prefix: str
    :param suffix: str
    :param decimals: int
    :param bar_length: int
    :return: _
    """
    format_str = "{0:." + str(decimals) + "f}"
    percent = format_str.format(100 * (iteration / float(total)))
    filled_length = int(round(bar_length * iteration / float(total)))
    bar = '#' * filled_length + '-' * (bar_length - filled_length)
    sys.stdout.write('\r%s |%s| %s%s %s\n' % (prefix, bar, percent, '%', suffix)),
    sys.stdout.flush()


def append_list_to_dic(list_from, dic_to):
    """
    append list to dic
    :param list_from: list
    :param dic_to: dic
    :return: bool
    """

    if len(list_from) != len(dic_to):
        return False

    for key in dic_to.keys():
        if type(dic_to[key]) is not list:
            return False

    # insert
    for index, key in enumerate(dic_to.keys()):
        dic_to[key].append(list_from[index])

    return True


def append_dic_of_all_key_list_value(dic, key, data):
    """
    append dic of all key list value
    :param dic: dic
    :param key: all
    :param data: all
    :return: bool
    """
    key_overlap = False

    if key in dic.keys():
        key_overlap = True
        dic[key].append(data)
    else:
        dic[key] = [data]

    return key_overlap


def read_df(df_path_left, df_name, df_type, reset_index=True):
    """
    read df
    :param df_path_left: str
    :param df_name: str
    :param df_type: str
    :param reset_index: bool
    :return: bool, df
    """
    df_path_full = df_path_left + df_name + '.' + df_type
    if not os.path.exists(df_path_full):
        return False, None

    if df_type == 'csv':
        target_df = pd.read_csv(df_path_full, encoding='euc-kr')
    elif df_type == 'pickle':
        target_df = pd.read_pickle(df_path_full)
    else:
        return False, None

    if reset_index:
        target_df = target_df.reset_index(drop=True)

    return True, target_df


def write_df(target_df, df_path_left, df_name, df_type, reset_index=True):
    """
    write df
    :param target_df: df
    :param df_path_left: str
    :param df_name: str
    :param df_type: str
    :param reset_index: bool
    :return: bool
    """
    df_path_left = make_dir_return_path(df_path_left)

    if reset_index:
        target_df = target_df.reset_index(drop=True)

    df_path_full = df_path_left + df_name + '.' + df_type
    if df_type == 'csv':
        target_df.to_csv(df_path_full, header=True, index=None, encoding='euc-kr')
    elif df_type == 'pickle':
        target_df.to_pickle(df_path_full)


def dump_json(target, save_path_left, save_name):
    """
    dump json
    :param target: all
    :param save_path_left: str
    :param save_name: str
    :return: _
    """
    config_path_full = save_path_left + save_name + '.json'

    with open(config_path_full, "w") as path:
        json.dump(target, path, indent=5)


def load_json(save_path_left, save_name):
    """
    load json
    :param save_path_left: str
    :param save_name: str
    :return: bool, all
    """
    save_path_full = save_path_left + save_name + '.json'
    if not os.path.exists(save_path_full):
        return False, None

    with open(save_path_full, "r") as path:
        target = json.load(path)

    return True, target
