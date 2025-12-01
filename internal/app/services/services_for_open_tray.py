from internal.common.func import get_platform, get_machine, has_file
from internal.common.kits.main_dirpath import mian_virtual_dirpath
from internal.common.kits.shell import shell_run_bin_process

#
CONFIG = {}

# 运行tray程序
def services_for_open_tray(_WINDOW, _webview_pid, _config):

    #
    global CONFIG
    CONFIG = _config

    platform = get_platform()
    machine = get_machine()
    # 相对路径直接运行
    if platform == "win":
        file_path = mian_virtual_dirpath("frontend") + "/tray/" + platform + "/" + "tray_" + machine + ".exe"
        pass
    else:
        file_path = mian_virtual_dirpath("frontend") + "/tray/" + platform + "/" + "tray_" + machine
        pass
    #
    if has_file(file_path):
        run_state = shell_run_bin_process(file_path, "-la")
        print("open_tray=", run_state, file_path)
        pass
    else:
        print("open_tray无对应文件：", file_path)
        pass
