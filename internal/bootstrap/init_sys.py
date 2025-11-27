from internal.bootstrap.init_tray import init_tray
from internal.common.main_dirpath import mian_virtual_dirpath
from internal.common.txt_data import txt_remove, txt_write
from internal.config import get_config
from internal.bootstrap.run_check_sys import run_check_sys
from internal.common.func import rand_range_string, print_log


# 程序主入口
def init_sys():
    # 获取前端资源路径
    frontend_dirpath = mian_virtual_dirpath("frontend")
    print(f"资源目录: {frontend_dirpath}")
    #
    CONFIG = get_config("run")
    #
    check_sys_state = run_check_sys()
    if check_sys_state:
        print_log("🍜 " + CONFIG["app"]["app_name"] + " => ", "v" + CONFIG["app"]["app_version"], CONFIG["app"]["author"], CONFIG["app"]["docs"] + "init_sys")
        # 设置一个临时的运行标记id
        running_id_filename = CONFIG["app"]["app_class"]+CONFIG["sys"]["running_id_filename"]
        txt_remove(running_id_filename)
        running_id = rand_range_string(64, 128)
        txt_write(running_id_filename, running_id)
        #
        init_tray()
    else:
        print("XXX Operation-SYS is Low：", check_sys_state, "last CPU " + str(CONFIG["check"]["min_cpu_cores"]) + " Cores, last RAM " + str(CONFIG["check"]["min_ram"]) + " GB, last Python " + str(CONFIG["check"]["min_python_version"]) + ", Flask-Port " + str(CONFIG["flask"]["port"]) + " .")
    return