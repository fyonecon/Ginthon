from internal.common.kits.main_dirpath import mian_virtual_dirpath
from internal.common.kits.txt_data import txt_remove, txt_write
from internal.config import get_config
from internal.bootstrap.run_check_sys import run_check_sys
from internal.bootstrap.init_window import init_window
from internal.common.func import rand_range_string, print_log, has_file, cache_path

# 代码习惯基于Golang。

# 程序主入口
def init_sys():
    # 获取前端资源路径
    cache_dirpath = cache_path() + "/" + get_config("func")["sys"]["cache_path_main_dir"]
    frontend_dirpath = mian_virtual_dirpath("frontend")
    print("### 两个重要目录 => ", {
        "frontend_dirpath": frontend_dirpath,
        "cache_dirpath": cache_dirpath,
        "frontend-launcher.png": has_file(frontend_dirpath+"/launcher.png"),
    })
    #
    CONFIG = get_config("")
    #
    check_sys_state = run_check_sys()
    if check_sys_state:
        print_log("=== " + CONFIG["app"]["app_name"] + " => ", "v" + CONFIG["app"]["app_version"], CONFIG["app"]["author"], CONFIG["app"]["docs"] + "init_sys")
        # 设置一个临时的运行标记id
        running_id_filename = CONFIG["sys"]["running_id_filename"]
        txt_remove(running_id_filename)
        running_id = rand_range_string(64, 128)
        txt_write(running_id_filename, running_id)
        #
        init_window()
    else:
        print("XXX Operation-SYS is Low：", check_sys_state, "last CPU " + str(CONFIG["check"]["min_cpu_cores"]) + " Cores, last RAM " + str(CONFIG["check"]["min_ram"]) + " GB, last Python " + str(CONFIG["check"]["min_python_version"]) + ", Flask-Port " + str(CONFIG["flask"]["port"]) + " .")
        # alert
    return