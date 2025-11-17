# Ginthon主入口
# 代码习惯基于Golang。

import multiprocessing

from common.config import init_config, read_config
from bootstrap.check_sys import check_sys
from bootstrap.run_flask import run_flask
from bootstrap.run_services import run_services

# 启动flask
def init_flask(config):
    run_flask(config)
    pass

# 启动后台服务
def init_services(config):
    run_services(config)
    pass

#
def ginthon(config):
    # 创建【多核多进程」任务
    process1 = multiprocessing.Process(target=init_flask(config))
    process2 = multiprocessing.Process(target=init_services(config))
    # 启动进程
    process1.start()
    process2.start()
    # 等待进程完成
    process1.join()
    process2.join()

    pass

# 读取配置文件+系统参数检测
def init_sys(config):
    print("🧐"+config["app_name"]+"=>", "\n", "v"+config["app_version"], config["author"], "\n", config["docs"]+"init_sys", "\n")
    check_sys_state = check_sys(config, "1")
    if check_sys_state:
        ginthon(config)
    else:
        print("❌ Operation-SYS is Low：", "last CPU "+str(config["min_cpu_cores"])+" Cores, last RAM "+str(config["min_ram"])+" GB, last Python "+str(config["min_python_version"])+", Flask-Port "+str(config["flask"]["port"])+" .")
    pass

# main
if __name__ == "__main__":
    print("\n")
    init_sys(init_config())
    print("\n")
    pass