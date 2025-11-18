import multiprocessing

from internal.run_pywebview import run_pywebview
from internal.watch_processes import watch_processes
from common.config import get_config
from internal.run_check_sys import run_check_sys
from internal.run_flask import run_flask
from internal.run_services import run_services

# 启动后台服务
def init_services():
    run_services()
    pass

# 启动web服务
def init_flask():
    run_flask()
    pass

# 启动窗口服务
def init_pywebview():
    run_pywebview()
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
    # 多文件共享值
    # set_txt_log()
    # 检测所有进程
    watch_processes(process1.pid, process2.pid, process3.pid)
    # 等待进程完成
    process1.join()
    process2.join()
    process3.join()

    pass

# 程序主入口
def run():
    CONFIG = get_config("run")
    #
    check_sys_state = run_check_sys()
    if check_sys_state:
        print("🍜 " + CONFIG["app"]["app_name"] + " => ", "v" + CONFIG["app"]["app_version"], CONFIG["app"]["author"], CONFIG["app"]["docs"] + "init_sys")
        ginthon()
    else:
        print("❌ Operation-SYS is Low：", check_sys_state, "last CPU " + str(CONFIG["check"]["min_cpu_cores"]) + " Cores, last RAM " + str(CONFIG["check"]["min_ram"]) + " GB, last Python " + str(CONFIG["check"]["min_python_version"]) + ", Flask-Port " + str(CONFIG["flask"]["port"]) + " .")
    pass