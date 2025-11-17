import threading
import time

from bootstrap.run_pywebview import run_pywebview
from common.func import get_time_ms, get_date
from common.time_interval import time_interval

#
CONFIG = {}

# 周期服务
def start_time_interval():
    print("周期服务1")
    def do_timer1():
        print("do_timer=1=", get_date("%Y-%m-%d %H:%M:%S"))
        pass
    time_interval(10, do_timer1, "run_service")

    pass

# pywebview窗口服务
def start_pywebview():
    print("视窗服务")
    run_pywebview()

    pass

# 启动服务
def run_services(config):
    # 读取配置信息
    global CONFIG
    CONFIG = config
    #
    time.sleep(2)
    print("✅服务=>", "\n", get_date("%Y-%m-%d %H:%M:%S"), "\n")

    # 创建线程
    t1 = threading.Thread(target=start_time_interval)
    t2 = threading.Thread(target=start_pywebview)

    # 启动线程
    t1.start()
    t2.start()

    # 等待线程结束
    t1.join()
    t2.join()

    print("❌服务运行结束，线程中断。")
    pass