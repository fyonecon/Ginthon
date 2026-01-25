# -*- coding: utf-8 -*-
from time import sleep

from internal.common.kits.main_dirpath import main_dirpath
from internal.common.kits.notice import notice
from internal.common.kits.txt_data import txt_data
from internal.config import get_config
from internal.bootstrap.run_check_sys import run_check_sys
from internal.bootstrap.init_window import init_window
from internal.common.func import func


# 代码习惯基于Golang。

# 程序主入口
def init_sys(cmd_model):
    # 获取前端资源路径
    print("### 核对重要目录 => ", {
        "frontend_dirpath": main_dirpath.virtual_dirpath("frontend"),
        "cache_dirpath": func.get_local_cache_path(),
        "data_dirpath": func.get_local_data_path(""),
        "frontend-launcher.png": func.has_file(main_dirpath.virtual_dirpath("frontend")+"/"+"icon.png"),
    })
    #
    CONFIG = get_config("", "")
    #
    check_sys_state = run_check_sys()
    if check_sys_state:
        func.print_log("=== " + CONFIG["app"]["app_name"] + " => ", "v" + CONFIG["app"]["app_version"], CONFIG["app"]["author"], CONFIG["app"]["docs"] + "init_sys")
        # 设置一个临时的运行标记id
        running_id_filename = CONFIG["sys"]["running_id_filename"]
        txt_data.remove(running_id_filename)
        running_id = func.rand_range_string(64, 128)
        txt_data.write(running_id_filename, running_id)
        #
        init_window(cmd_model)
    else:
        notice.send("⚠️", "Can't open the software.")
        sleep(1)
        print("XXX Operation-SYS is Low：", check_sys_state, "last CPU " + str(CONFIG["check"]["min_cpu_cores"]) + " Cores, last RAM " + str(CONFIG["check"]["min_ram"]) + " GB, last Python " + str(CONFIG["check"]["min_python_version"]) + ", Flask-Port " + str(CONFIG["flask"]["port"]) + " .")
        # alert
        exit(403) # 出现错误就直接关闭程序
    return