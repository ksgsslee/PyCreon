def make_input_value_all(dic_input_value_default, dic_input_value):
    dic_input_value_default_copy = dic_input_value_default.copy()
    for n_key, value in dic_input_value.items():
        dic_input_value_default_copy[n_key] = value
    return dic_input_value_default_copy


def make_filename(lis_input_value_make_filename, dic_input_value_all):
    s_ret = ''

    for n_index_1, n_value_1 in enumerate(lis_input_value_make_filename):
        if dic_input_value_all[n_value_1] is None:
            return False, s_ret

        if n_index_1 == len(lis_input_value_make_filename) - 1:
            s_ret += str(dic_input_value_all[n_value_1])
        else:
            s_ret += str(dic_input_value_all[n_value_1]) + '_'

    return True, s_ret
