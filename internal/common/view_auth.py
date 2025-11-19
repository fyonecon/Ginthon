
CONFIG = {}

# 生成view_auth
def make_view_auth(url, config):
    global CONFIG
    CONFIG = config
    #
    return "123#@view_auth"

# 校验view_auth值
def check_view_auth(view_auth):
    return True