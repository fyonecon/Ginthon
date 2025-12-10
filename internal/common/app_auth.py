from internal.common.func import str_encode, md5, rand_range_string, get_time_ms, str_decode
from internal.common.kits.txt_data import txt_read
from internal.config import get_config

# 生产token
# 依赖于赋值参数，可复用
def make_rand_token(app_class, salt_str, timeout_s, config):
    CONFIG = config
    #
    if len(app_class)==0:
        app_class = CONFIG["app"]["app_class"]
        pass
    if timeout_s < 10:
        timeout_s = 10
        pass
    #
    new_str = app_class+"#@"+md5(salt_str+"_-@!_"+app_class)+"#@"+str(get_time_ms())+"#@"+str(timeout_s*1000)+"#@"+rand_range_string(4, 6)
    #
    return str_encode(new_str, CONFIG["pywebview"]["secret_key"])

# 校验token
def check_rand_token(app_class, salt_str, config, check_str):
    CONFIG = config
    #
    if len(app_class) == 0:
        app_class = CONFIG["app"]["app_class"]
        pass
    try:
        old_str = str_decode(check_str, CONFIG["pywebview"]["secret_key"])
        the_salt_str = md5(salt_str+"_-@!_"+app_class)
        the_old_str = old_str.split("#@")
        _app_class = the_old_str[0]
        _salt_str = the_old_str[1]
        _old_time_ms = int(the_old_str[2])
        _timeout_ms = int(the_old_str[3])
        #
        OK = app_class == _app_class and the_salt_str == _salt_str and (_old_time_ms + _timeout_ms) >= get_time_ms()
        if OK:
            return True, "参数已匹配"
        else:
            return False, "Token参数不匹配"
    except:
        return False, "Token参数错误"

# 生成rand_id
# 依赖于每次启动程序时生成的随机id，不可复用或跨软件
def make_rand_id(config):
    CONFIG = config
    #
    running_id_filename = CONFIG["sys"]["running_id_filename"]
    running_id = txt_read(running_id_filename)
    #
    return str_encode(running_id, CONFIG["pywebview"]["secret_key"])

# 校验rand_id值
def check_rand_id(view_rand_id):
    CONFIG = get_config("", "")
    #
    running_id_filename = CONFIG["sys"]["running_id_filename"]
    running_id = txt_read(running_id_filename)
    return str_encode(running_id, CONFIG["pywebview"]["secret_key"]) == view_rand_id

# 生成view_auth
# 依赖于每次启动程序时生成的随机id，不可复用或跨软件
def make_auth(config):
    CONFIG = config
    #
    app_class = CONFIG["app"]["app_class"]
    running_id_filename = CONFIG["sys"]["running_id_filename"]
    running_id = txt_read(running_id_filename)
    return md5(app_class+"#@"+running_id)

# 校验view_auth值
def check_auth(view_auth):
    CONFIG = get_config("", "")
    #
    app_class = CONFIG["app"]["app_class"]
    running_id_filename = CONFIG["sys"]["running_id_filename"]
    running_id = txt_read(running_id_filename)
    return md5(app_class+"#@"+running_id) == view_auth
