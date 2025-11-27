import threading
import os
from time import sleep

from internal.bootstrap.run_check_sys import check_port_occupied
from internal.common.func import print_log
from internal.common.time_interval import do_time_interval
from internal.common.watch_pid import kill_process_by_pid
from internal.config import get_config

#
CONFIG = {}
HOST_STATE = 1

# 检测视窗服务是否可用，不可用则主动退出状态栏托盘程序
def service_for_ping_window():
    global HOST_STATE
    tag = "service_for_ping_window"
    def do_timer():
        global HOST_STATE
        main_pid = os.getpid()
        # 判断端口是否被占用
        flask_port = CONFIG["flask"]["port"]
        flask_port_state = check_port_occupied('127.0.0.1', flask_port, timeout=2)
        if flask_port_state: # 占用
            HOST_STATE = 1
            pass
        else: # 空闲
            host = "127.0.0.1:"+str(flask_port)
            if HOST_STATE >= 2:
                # Exit
                print("🔴 主动退出程序=视窗可能未启动=PID=", main_pid, HOST_STATE, host)
                kill_process_by_pid(main_pid)
                #
                pass
            else:
                print("🔴 程序正在运行自检...（可能是因为视窗程序未启动）", main_pid, HOST_STATE, host)
                HOST_STATE = HOST_STATE + 1
                pass
            pass
        #
        pass
    do_time_interval(2, do_timer, tag, CONFIG)
    pass

# 后台服务
def run_service():
    print_log("### run_service")

    # 读取配置信息
    global CONFIG
    CONFIG = get_config("run_services")
    #
    # sleep(1)

    # 创建线程
    t1 = threading.Thread(target=service_for_ping_window, daemon=True)

    # 启动线程
    t1.start()
    # t2.start()

    # 等待线程结束
    t1.join()
    # t2.join()

    print("XXX 服务运行结束，线程中断。")

    pass