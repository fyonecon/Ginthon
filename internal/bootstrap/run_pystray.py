from internal.common.config import get_config
from internal.common.func import print_log

#
CONFIG = {}

# 状态托盘服务
def run_pystray():
    # 读取配置信息
    global CONFIG
    CONFIG = get_config("run_stray")
    #
    print_log("✅ 状态托盘 => ")
    pass