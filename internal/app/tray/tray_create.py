# -*- coding: utf-8 -*-

import os
from time import sleep

import pystray
import requests
from PIL import Image
import io

from internal.common.app_auth import make_rand_token, make_auth
from internal.common.func import print_log
from internal.common.kits.ICON import ICON_Binary
from internal.common.kits.watch_pid import kill_process_by_pid
from internal.common.translate import get_translate
from internal.config import get_config

#
CONFIG = {}

# 请求window视图的状态
def request_window(do):
    global CONFIG
    CONFIG = get_config("", "")

    #
    app_class = CONFIG["app"]["app_class"]
    salt_str = "pystray2025"
    timeout_s = 2*365*24*60*60
    tray_rand_token = make_rand_token(app_class, salt_str, timeout_s, CONFIG)

    # API
    url = CONFIG["pytray"]["api_url"]+"/"+tray_rand_token
    # 请求数据
    data = {
        "app_class": CONFIG["app"]["app_class"],
        "app_version": CONFIG["app"]["app_version"],
        "do": do,
        "view_auth": make_auth(CONFIG)
    }
    headers = {
        "Content-Type": "application/json",
        "User-Agent": CONFIG["app"]["app_class"] + CONFIG["app"]["app_version"],
    }
    # POST
    response = requests.post(url=url, timeout=4, headers=headers, json=data)
    back_data = response.json()
    print_log("back_data=", back_data)
    #
    state = back_data["state"]
    msg = back_data["msg"]
    #
    return state, msg, back_data

# 托盘菜单操作
def on_show_or_hide(icon, item_text):
    try:
        state, msg, back_data = request_window("app@show_or_hide")
        print_log("接口返回：", [state, msg])
        if state == 1:
            #
            pass
        elif state == 0:
            icon.notify(title="空数据", message=msg)
            pass
        else:
            icon.notify(title="未知状态："+str(state), message=msg)
            pass
        pass
    except:
        print("on_show_or_hide 错误：", "接口不通，可能是视窗主程序未启动")
        pass
    pass

# 关于
# 1 成功
def on_about(icon, item_text):
    try:
        state, msg, back_data = request_window("app@about")
        print_log("接口返回：", [state, msg])
        if state == 1:
            #
            pass
        elif state == 0:
            icon.notify(title="空数据", message=msg)
            pass
        else:
            icon.notify(title="未知状态：" + str(state), message=msg)
            pass
        pass
    except:
        print("on_about 错误：", "接口不通，可能是视窗主程序未启动")
        pass
    pass

# 退出程序
# 1 exit
def on_exit(icon, item):
    try:
        state, msg, back_data = request_window("app@exit")
        print_log("接口返回：", [state, msg])
        if state == 1:
            try:
                sleep(1)
                icon.stop()
            except:
                main_pid = os.getpid()
                kill_process_by_pid(main_pid)
            pass
        elif state == 0:
            icon.notify(title="空数据", message=msg)
            pass
        else:
            icon.notify(title="未知状态：" + str(state), message=msg)
        pass
    except:
        print("on_exit 错误：", "接口不通，可能是视窗主程序未启动")
        sleep(1)
        main_pid = os.getpid()
        kill_process_by_pid(main_pid)
        pass
    pass

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


# 创建tray
# mac、win、linux创建时都会调用此函数，但不会被window.py直接调用
def tray_create():
    #
    global CONFIG
    CONFIG = get_config("", "")

    # 创建菜单
    menu = pystray.Menu(
        pystray.MenuItem(text="" + get_translate("show_window"), action=on_show_or_hide, default=True),
        pystray.Menu.SEPARATOR,
        # pystray.MenuItem(text="❗️ 关于"+CONFIG["app"]["app_name"], action=on_about, default=False),
        # pystray.Menu.SEPARATOR,
        pystray.MenuItem(text="🔴 " + get_translate("exit_app"), action=on_exit, radio=False, default=False)
    )

    # 创建托盘图标
    icon = pystray.Icon(
        CONFIG["app"]["app_name"],  # app_name
        load_icon(ICON_Binary),  # 图标
        "显示、隐藏、退出 " + CONFIG["app"]["app_name"],  # hover tips
        menu  # 菜单
    )

    # 托盘
    icon.run()

    pass
