import threading

from internal.app.services.services_for_open_tray import services_for_open_tray
from internal.app.services.services_for_time_interval import services_for_time_interval
from internal.config import get_config
from internal.common.func import get_date

#
CONFIG = {}

# 启动服务
def run_services(window, webview_pid, config):
    print("### 后台服务 => ", get_date("%Y-%m-%d %H:%M:%S"))

    # 读取配置信息
    global CONFIG
    CONFIG = config
    #

    # 创建线程
    t1 = threading.Thread(target=services_for_time_interval, daemon=True, args=(window, webview_pid, CONFIG))
    t2 = threading.Thread(target=services_for_open_tray, daemon=True, args=(window, webview_pid, CONFIG))

    # 启动线程
    t1.start()
    t2.start()

    # 等待线程结束
    t1.join()
    t2.join()

    print("XXX 服务运行结束，线程中断。")
    pass