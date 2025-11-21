from internal.config import get_config
from internal.common.func import print_log

#
CONFIG = {}

# 状态托盘服务
def run_pystray():
    # 读取配置信息
    global CONFIG
    CONFIG = get_config("run_stray")
    #
    print_log("✅ 状态托盘 => ")

    # menu = (MenuItem('菜单1', lambda: print("点击了菜单1")), MenuItem('菜单2', lambda: print("点击了菜单2")))
    # image = Image.open(CONFIG["pystray"]["icon"])
    # icon = pystray.Icon("name", image, "鼠标移动到\n托盘图标上\n展示内容", menu)
    # icon.run()

    #
    pass