# -*- coding: utf-8 -*-

from internal.common.func import has_file, get_platform
from internal.common.kits.main_dirpath import mian_virtual_dirpath
from internal.common.kits.notice import send_notice
from internal.common.kits.shell import shell_run_bin_process

#
CONFIG = {}

# 调用命令行打开二进制文件
def tray_open(window, webview_pid, config):
    #
    global CONFIG
    CONFIG = config

    # 兼容处理
    plt = get_platform()
    if plt == "mac" or plt == "linux":
        file = "Tray"  # 源文件路径
        pass
    else:
        file = "Tray.exe"  # 源文件路径
        pass
    # 命令行运行
    file_path = mian_virtual_dirpath("frontend") + "/tray/" + file
    #
    try:
        if has_file(file_path):
            run_state = shell_run_bin_process(file_path, "-la")
            print("open_tray=", run_state, file_path)
            pass
        else:
            print("XXX open_tray无对应文件：", file_path)
            pass
        pass
    except:
        send_notice("⚠️", "Tray can't Open.")
        pass