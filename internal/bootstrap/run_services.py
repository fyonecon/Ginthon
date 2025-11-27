import threading

from time import sleep

from zope.interface.common.builtins import IFile

from internal.common._7z import _7z_remove_dir, _7z_unarchive
from internal.common.main_dirpath import mian_virtual_dirpath
from internal.common.shell import shell_run_bin_process
from internal.config import get_config
from internal.common.func import get_date, print_log, main_path, get_platform, cache_path, has_file, get_machine
from internal.common.time_interval import do_time_interval

#
CONFIG = {}

# 运行tray程序
def services_for_open_tray():
    platform = get_platform()
    machine = get_machine()
    # 文件路径
    # output_dirpath最终效果=/Users/xxx/Library/Caches/top.datathink.Ginthon/running/tray/mac/mac/tray
    _cache_path = cache_path() + "/" + get_config("func")["sys"]["cache_path_main_dir"]  # 结尾无/
    if platform == "win":
        archive_file = mian_virtual_dirpath("frontend") + "/tray/" + platform + "/" + "tray_" + machine + ".exe.7z"  # 文件
        pass
    else:
        archive_file = mian_virtual_dirpath("frontend") + "/tray/" + platform + "/" + "tray_" + machine + ".7z"  # 文件
        pass
    output_dirpath = _cache_path + "/running/tray/" + platform + ""  # 结尾无/
    # 解压
    remove_dir_state, remove_dir_msg = _7z_remove_dir(output_dirpath) # 删除老文件
    _7z_unarchive_state, _7z_unarchive_msg = _7z_unarchive(archive_file, output_dirpath)
    #
    print("解压文件=", [has_file(archive_file), remove_dir_msg, _7z_unarchive_msg])
    # 运行程序
    if _7z_unarchive_state:
        # 运行
        if platform == "win":
            root_path = output_dirpath + "/" + "tray_" + machine+".exe"
            pass
        else:
            root_path = output_dirpath + "/" + "tray_" + machine
            pass
        run_state = shell_run_bin_process(root_path, "-la")
        print_log("services_for_open_tray=", run_state, root_path)
        pass
    else:
        print("解压文件时出错：", [remove_dir_msg, _7z_unarchive_msg])
        pass
    pass

# 周期服务，默认10s
def services_for_time_interval():
    sleep(1)
    tag = "run_service_1"
    print_log("🚩周期服务：", "tag="+tag)
    #
    def do_timer1():
        print_log("do_timer=1=", get_date("%Y-%m-%d %H:%M:%S"))
        #
        pass
    do_time_interval(6, do_timer1, tag, CONFIG)
    pass

# 启动服务
def run_services(window, pid):
    print("### 后台服务 => ", get_date("%Y-%m-%d %H:%M:%S"))

    # 读取配置信息
    global CONFIG
    CONFIG = get_config("run_services")
    #

    # 创建线程
    t1 = threading.Thread(target=services_for_time_interval, daemon=True)
    t2 = threading.Thread(target=services_for_open_tray, daemon=True)

    # 启动线程
    t1.start()
    t2.start()

    # 等待线程结束
    t1.join()
    t2.join()

    print("XXX 服务运行结束，线程中断。")
    pass