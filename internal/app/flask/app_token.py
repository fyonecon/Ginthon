from internal.common.app_auth import rand_token
from internal.common.func import func
from internal.common.request_data import request_data
from internal.config import get_config


# 校验
def check_app_token(request, _salt = ""):
    CONFIG = get_config("", "")
    app_token = request_data.input(request, "app_token")
    app_class = CONFIG["app"]["app_class"]
    salt_str = "auth-2025" + _salt
    app_token_state, _ = rand_token.check(app_class, func.md5(salt_str + "nbPlus"), CONFIG, app_token)
    #
    return app_token_state


# 生成
def make_app_token(_salt = ""):
    CONFIG = get_config("", "")
    app_class = CONFIG["app"]["app_class"]
    salt_str = "auth-2025" + _salt
    timeout_s = 2 * 365 * 24 * 3600
    app_token = rand_token.make(app_class, func.md5(salt_str + "nbPlus"), timeout_s, CONFIG)  # page刷新时会生成一个新的
    #
    return app_token