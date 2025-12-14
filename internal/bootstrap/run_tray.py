from internal.app.tray.tray_open import tray_open

#
CONFIG = {}

# 创建状态栏托盘
def run_tray(window, webview_pid, config):
    # 读取配置信息
    global CONFIG
    CONFIG = config

    #
    tray_open(window, webview_pid, config)

    pass