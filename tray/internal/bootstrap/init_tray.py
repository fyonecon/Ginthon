import os
import pystray
from PIL import Image
import threading

from internal.app.interval import start_internal
from internal.app.pystray import on_show_or_hide, on_exit, on_about
from internal.app.service import run_service
from internal.common.func import print_log
from internal.config import get_config

#
CONFIG = {}

# 图标
def load_icon():
    if os.path.exists("./frontend/launcher.png"):
        image = Image.open("./frontend/launcher.png")
        return image.resize((64, 64), Image.Resampling.LANCZOS)
    else:
        # 创建默认图标
        image = Image.new('RGB', (64, 64), 'blue')
        return image



# 启动
def run_pystray():

    # 创建菜单
    menu = pystray.Menu(
        pystray.MenuItem(text="显示 或 隐藏", action=on_show_or_hide, default=True),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem(text="关于"+CONFIG["app"]["app_name"], action=on_about, default=False),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem(text="🔴 退出程序", action=on_exit, radio=False, default=False)
    )

    # 创建托盘图标
    icon = pystray.Icon(
        CONFIG["app"]["app_name"],  # app_name
        load_icon(),  # 图标
        "显示、隐藏、退出 " + CONFIG["app"]["app_name"],  # hover tips
        menu  # 菜单
    )

    # 创建线程
    t1 = threading.Thread(target=run_service, daemon=True)

    # 启动线程
    t1.start()

    # 托盘
    icon.run()

    # 等待线程结束
    t1.join()

    pass


# 状态栏托盘（pystray必须运行在主线程上）
def init_tray():
    global CONFIG
    CONFIG = get_config()
    print_log("✅ 状态栏托盘 ")

    #
    run_pystray()

    pass