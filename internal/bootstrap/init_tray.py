import os
import pystray
from PIL import Image
import io
import threading

from internal.common.kits.ICON import ICON_Binary
from internal.app.pystray import on_show_or_hide, on_exit, on_about
from internal.app.service import run_service
from internal.common.func import print_log
from internal.common.translate import get_translate
from internal.config import get_config

#
CONFIG = {}

# 图标
def load_icon(icon_binary):
    # 适用图片文件
    # if os.path.exists("./frontend/launcher.png"): # mac/linux .png, win .ico
    #     image = Image.open("./frontend/launcher.png")
    #     return image.resize((64, 64), Image.Resampling.LANCZOS)
    # else:
    #     # 创建默认图标
    #     image = Image.new('RGB', (64, 64), 'blue')
    #     return image

    # 图片转成二进制
    # with open("./frontend/launcher.png", "rb") as f:
    #     icon_binary = f.read()

    # 使用 BytesIO 将二进制数据转换为图像（win、mac、linux均可使用）
    image = Image.open(io.BytesIO(icon_binary))
    # 确保图像尺寸合适（推荐 16x16, 32x32, 64x64, 128x128）
    image = image.resize((128, 128), Image.Resampling.LANCZOS)
    return image


# 启动
def run_pystray():

    # 创建菜单
    menu = pystray.Menu(
        pystray.MenuItem(text="❇️ "+get_translate("show_window"), action=on_show_or_hide, default=True),
        pystray.Menu.SEPARATOR,
        # pystray.MenuItem(text="❗️ 关于"+CONFIG["app"]["app_name"], action=on_about, default=False),
        # pystray.Menu.SEPARATOR,
        pystray.MenuItem(text="🔴 "+get_translate("exit_app"), action=on_exit, radio=False, default=False)
    )

    # 创建托盘图标
    icon = pystray.Icon(
        CONFIG["app"]["app_name"],  # app_name
        load_icon(ICON_Binary),  # 图标
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
    print_log("### 状态栏托盘 ")

    #
    run_pystray()

    pass