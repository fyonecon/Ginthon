# Ginthon主入口
# 代码习惯基于Golang。

import multiprocessing

from bootstrap.run_pywebview import run_pywebview
from bootstrap.watch_processes import watch_processes
from common.config import init_config
from bootstrap.run_check_sys import run_check_sys
from bootstrap.run_flask import run_flask
from bootstrap.run_services import run_services

#
CONFIG = init_config()

# 启动后台服务
def init_services():
    run_services(CONFIG)
    pass

# 启动web服务
def init_flask():
    run_flask(CONFIG)
    pass

# 启动窗口服务
def init_pywebview():
    run_pywebview(CONFIG)
    pass

#
def ginthon():
    # 创建【多核多进程」任务。注意已有顺序不要变
    process1 = multiprocessing.Process(target=init_services)
    process2 = multiprocessing.Process(target=init_flask)
    process3 = multiprocessing.Process(target=init_pywebview)
    # 启动进程
    process1.start()
    process2.start()
    process3.start()
    # 检测所有进程
    processes = (process1, process2, process3) # 顺序和容量都不可变
    watch_processes(processes)
    # 等待进程完成
    process1.join()
    process2.join()
    process3.join()

    pass

# 读取配置文件+系统参数检测
def check_sys():
    check_sys_state = run_check_sys(CONFIG, "1")
    if check_sys_state:
        print("🧐 " + CONFIG["app_name"] + " => ", "v" + CONFIG["app_version"], CONFIG["author"],
              CONFIG["docs"] + "init_sys")
        ginthon()
    else:
        print("❌ Operation-SYS is Low：", check_sys_state, "last CPU "+str(CONFIG["min_cpu_cores"])+" Cores, last RAM "+str(CONFIG["min_ram"])+" GB, last Python "+str(CONFIG["min_python_version"])+", Flask-Port "+str(CONFIG["flask"]["port"])+" .")
    pass

# main
if __name__ == "__main__":
    check_sys()
    print("\n")
    pass