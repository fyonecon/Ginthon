import threading

from time import sleep
from internal.config import get_config
from internal.common.func import get_date, print_log
from internal.common.time_interval import do_time_interval

#
CONFIG = {}

# 周期服务，默认10s
def services_for_time_interval():
    tag = "run_service_1"
    print_log("🚩周期服务：", "tag="+tag)
    #
    def do_timer1():
        print_log("do_timer=1=", get_date("%Y-%m-%d %H:%M:%S"))
        #
        pass
    do_time_interval(6, do_timer1, tag, CONFIG)
    pass

# 启动服务
def run_services():
    print_log("✅ 后台服务 => ", get_date("%Y-%m-%d %H:%M:%S"))

    # 读取配置信息
    global CONFIG
    CONFIG = get_config("run_services")
    #
    sleep(2)

    # 创建线程
    t1 = threading.Thread(target=services_for_time_interval)

    # 启动线程
    t1.start()
    # t2.start()

    # 等待线程结束
    t1.join()
    # t2.join()

    print("❌ 服务运行结束，线程中断。")
    pass