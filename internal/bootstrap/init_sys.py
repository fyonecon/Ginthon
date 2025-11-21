
from internal.config import get_config
from internal.bootstrap.run_check_sys import run_check_sys
from internal.bootstrap.init_window import init_window
from internal.common.func import print_log


# 程序主入口
def init_sys():
    CONFIG = get_config("run")
    #
    check_sys_state = run_check_sys()
    if check_sys_state:
        print_log("🍜 " + CONFIG["app"]["app_name"] + " => ", "v" + CONFIG["app"]["app_version"], CONFIG["app"]["author"], CONFIG["app"]["docs"] + "init_sys")
        init_window()
    else:
        print("❌ Operation-SYS is Low：", check_sys_state, "last CPU " + str(CONFIG["check"]["min_cpu_cores"]) + " Cores, last RAM " + str(CONFIG["check"]["min_ram"]) + " GB, last Python " + str(CONFIG["check"]["min_python_version"]) + ", Flask-Port " + str(CONFIG["flask"]["port"]) + " .")
    return