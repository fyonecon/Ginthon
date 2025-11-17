import threading
from time import sleep

from common.func import get_date
from bootstrap.start_time_interval import do_time_interval

#
CONFIG = {}

# 周期服务
def start_time_interval():
    tag = "run_service_1"
    print("🚩周期服务：", "tag="+tag)
    def do_timer1():
        print("do_timer=1=", get_date("%Y-%m-%d %H:%M:%S"))
        pass
    do_time_interval(10, do_timer1, tag, CONFIG)

    pass

# 启动服务
def run_services(config):
    print("✅ 后台服务 => ", get_date("%Y-%m-%d %H:%M:%S"))

    # 读取配置信息
    global CONFIG
    CONFIG = config
    #
    sleep(2)

    # 创建线程
    t1 = threading.Thread(target=start_time_interval)

    # 启动线程
    t1.start()

    # 等待线程结束
    t1.join()

    print("❌服务运行结束，线程中断。")
    pass