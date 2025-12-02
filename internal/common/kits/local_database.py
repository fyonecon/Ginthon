# 简单的本地数据库（k-v型数据库）
# 对称加密

import os.path

from internal.common.func import cache_path, md5, str_encode, has_file, str_decode, get_time_s, url_encode, has_dir, \
    print_log
from internal.config import get_config

# 截取固定长度的字符串，从第1位
def truncate_string(text, length):
    if len(text) <= length:
        return text
    return text[:length]

#
CONFIG = get_config()
_cache_path = cache_path() + "/" + CONFIG["sys"]["cache_path_main_dir"] # 结尾无/
local_path = _cache_path+"/local_database/" # /结尾
code_key = truncate_string("gt-py3_2025@localdatabase", 16) # 大于16位
code_salt = "2025"
#

# 设置或更新 健值对 数据
def local_database_set_data(data_key:str, data_value:str, data_timeout_s:int):
    filename = CONFIG["app"]["app_class"] + "local_"+md5(data_key+code_salt)+".lcl"
    the_file = local_path+filename
    timer = get_time_s() + data_timeout_s # 截止日期
    _value = url_encode(data_key) + "\n" + str(timer) + "\n" + str_encode(data_value, code_key)  # 写入3行数据
    if not os.path.exists(local_path):
        os.makedirs(local_path, exist_ok=True)
        pass
    with open(the_file, "w", encoding="utf-8") as file: # 会覆盖老数据
        file.write(_value)
    return data_value

# 读取数据
def local_database_get_data(data_key:str):
    filename = CONFIG["app"]["app_class"] + "local_" + md5(data_key + code_salt) + ".lcl"
    the_file = local_path + filename
    if has_file(the_file):
        _key = ""
        _timer = ""
        _value = ""
        with open(the_file, 'r', encoding='utf-8') as f:
            line_num = 1
            while True:
                line = f.readline()
                if not line:  # 读到文件末尾
                    break
                print_log(f'第{line_num}行: {line.strip()}')
                the_line_num = line_num
                the_line_txt = line.strip()
                if the_line_num == 1:
                    _key = the_line_txt
                    pass
                elif the_line_num == 2:
                    _timer = the_line_txt
                    pass
                elif the_line_num == 3:
                    _value = the_line_txt
                else:
                    break
                line_num += 1
            pass
        # 兼容处理
        try:
            _last_time = int(_timer)
            pass
        except:
            _last_time = _timer
            pass
        #
        now_time = get_time_s()
        if _last_time <= now_time:
            return str_decode(_value, code_key), 1
        else:
            return "", local_database_del_data(data_key)
    else:
        return "", -1

# 删除数据（删除文件）
def local_database_del_data(data_key:str):
    filename = CONFIG["app"]["app_class"] + "local_" + md5(data_key + code_salt) + ".lcl"
    the_file = local_path + filename
    if has_file(the_file):
        os.remove(the_file)
        return 1
    else:
        return -1