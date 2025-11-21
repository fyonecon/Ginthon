from window.internal.common.func import str_encode, md5
from window.internal.common.txt_data import txt_read
from window.internal.config import get_config

def make_view_rand_id(url, config):
    CONFIG = config
    #
    running_id_filename = CONFIG["sys"]["running_id_filename"]
    running_id = txt_read(running_id_filename)
    return str_encode(running_id, CONFIG["pywebview"]["secret_key"])

# 生成view_auth
def make_view_auth(url, config):
    CONFIG = config
    #
    running_id_filename = CONFIG["sys"]["running_id_filename"]
    running_id = txt_read(running_id_filename)
    return md5(CONFIG["app"]["app_class"]+"#@"+running_id)

# 校验view_rand_id值
def check_view_rand_id(view_rand_id):
    CONFIG = get_config()
    #
    running_id_filename = CONFIG["sys"]["running_id_filename"]
    running_id = txt_read(running_id_filename)
    return str_encode(running_id, CONFIG["pywebview"]["secret_key"]) == view_rand_id

# 校验view_auth值
def check_view_auth(view_auth):
    CONFIG = get_config()
    #
    running_id_filename = CONFIG["sys"]["running_id_filename"]
    running_id = txt_read(running_id_filename)
    return md5(CONFIG["app"]["app_class"]+"#@"+running_id) == view_auth
