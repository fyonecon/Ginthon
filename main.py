# Ginthon主入口
# 代码习惯基于Golang。

import multiprocessing

from bootstrap.check_sys import check_sys
from bootstrap.run_flask import run_flask
from bootstrap.run_services import run_services
from common.global_data import GlobalData


# 启动flask
def init_flask():
    run_flask()
    pass

# 启动后台服务
def init_services():
    run_services()
    pass

#
def ginthon():
    # 创建【多核多进程」任务
    process1 = multiprocessing.Process(target=init_flask)
    process2 = multiprocessing.Process(target=init_services)
    # 启动进程
    process1.start()
    process2.start()
    # 等待进程完成
    process1.join()
    process2.join()

    pass

# 读取配置文件+系统参数检测
def init_sys():
    print("🧐"+GlobalData["app_name"]+"=>", "\n", "v"+GlobalData["app_version"], GlobalData["author"], "\n", GlobalData["docs"]+"init_sys", "\n")
    check_sys_state = check_sys("1")
    if check_sys_state:
        ginthon()
    else:
        print("❌ Operation-SYS is Low：", "last CPU "+str(GlobalData["min_cpu_cores"])+" Cores, last RAM "+str(GlobalData["min_ram"])+" GB, last Python "+str(GlobalData["min_python_version"])+", Flask-Port "+str(GlobalData["flask"]["port"])+" .")
    pass

# main
if __name__ == "__main__":
    print("\n")
    init_sys()
    print("\n")
    pass