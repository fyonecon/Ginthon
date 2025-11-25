import threading
from time import sleep

from internal.common.time_interval import do_time_interval
from internal.config import get_config

#
CONFIG = {}

#
def internal_for_window_alive():
    tag = "window_alive_1"
    print("🚩周期服务：", "tag=" + tag)

    #
    def request_window_alive(do):
        url = ""
        pass

    #
    def do_timer1():
        print("周期：", tag)
        #
        pass

    do_time_interval(5, do_timer1, tag, CONFIG)
    pass

#
def start_internal():
    print("start internal")
    # 读取配置信息
    global CONFIG
    CONFIG = get_config("start_internal")

    sleep(2)

    # 创建线程
    t1 = threading.Thread(target=internal_for_window_alive, daemon=True)

    # 启动线程
    t1.start()
    # t2.start()

    # 等待线程结束
    t1.join()
    # t2.join()

    print("❌ 服务运行结束，线程中断。")

    pass