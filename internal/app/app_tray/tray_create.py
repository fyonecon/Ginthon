# -*- coding: utf-8 -*-

import os
import threading
import warnings
from time import sleep

import pystray
import requests
import urllib3
from PIL import Image
import io

from internal.bootstrap.bootstrap_check_sys import check_port_occupied
from internal.common.app_auth import rand_token, view_auth
from internal.common.func import func
from internal.common.kits.ICON import ICON_Binary
from internal.common.kits.time_interval import time_interval
from internal.common.kits.watch_processes import watch_processes
from internal.config import get_config

#
CONFIG = {}
HAS_START = 0 # 是否成功Ping过
HOST_STATE = 1

# 辅助函数
class tray_create_func:

    # 检测视窗服务是否可用，不可用则主动退出状态栏托盘程序
    @staticmethod
    def tray_ping_window():
        global HAS_START
        global HOST_STATE
        tag = "tray_ping_window"

        def do_timer():
            global HAS_START
            global HOST_STATE
            main_pid = os.getpid()
            # 判断端口是否被占用
            flask_port = CONFIG["flask"]["port"]
            flask_port_state = check_port_occupied('127.0.0.1', flask_port, timeout=1)
            if flask_port_state:  # 占用
                HAS_START = 1
                HOST_STATE = 1
                pass
            else:  # 空闲
                host = "127.0.0.1:" + str(flask_port)
                if HOST_STATE >= 1:
                    # Exit
                    print("🔴 主动退出程序=视窗可能未启动=PID=", main_pid, HOST_STATE, host)
                    watch_processes.kill_process_by_pid(main_pid)
                    #
                    pass
                else:
                    print("🔴 程序正在运行自检...（可能是因为视窗程序未启动）", main_pid, HOST_STATE, host)
                    HOST_STATE = HOST_STATE + 1
                    pass
                pass
            #
            pass

        #
        do_timer()
        time_interval.do_time_interval(0, do_timer, tag, CONFIG)
        pass

    # 请求window视图的状态
    @staticmethod
    def request_window(do):
        global CONFIG
        CONFIG = get_config("", "")

        #
        app_class = CONFIG["app"]["app_class"]
        salt_str = "pystray2025"
        timeout_s = 2 * 365 * 24 * 60 * 60
        tray_rand_token = rand_token.make(app_class, salt_str, timeout_s, CONFIG)

        # API
        url = CONFIG["pytray"]["api_url"] + "/" + tray_rand_token
        # 请求数据
        data = {
            "app_class": CONFIG["app"]["app_class"],
            "app_version": CONFIG["app"]["app_version"],
            "do": do,
            "view_auth": view_auth.make(CONFIG)
        }
        headers = {
            "Content-Type": "application/json",
            "User-Agent": CONFIG["app"]["app_class"] + CONFIG["app"]["app_version"],
        }
        # POST
        func.print_log("url=", url, data)
        response = requests.post(url=url, timeout=4, headers=headers, json=data, verify=False)  # verify=False忽略SSL证书验证
        back_data = response.json()
        func.print_log("back_data=", back_data)
        #
        state = back_data["state"]
        msg = back_data["msg"]
        #
        return state, msg, back_data

    # 托盘菜单操作
    @staticmethod
    def on_show_or_hide(icon, item_text):
        try:
            state, msg, back_data = tray_create_func.request_window("app@show_or_hide")
            func.print_log("接口返回：", [state, msg])
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
        except Exception as err:
            func.print_log(err)
            print("on_show_or_hide 错误：", "接口不通，可能是视窗主程序未启动 或 api不能访问")
            pass
        pass

    # 关于
    # 1 成功
    @staticmethod
    def on_about(icon, item_text):
        try:
            state, msg, back_data = tray_create_func.request_window("app@about")
            func.print_log("接口返回：", [state, msg])
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
    @staticmethod
    def on_exit(icon, item):
        try:
            state, msg, back_data = tray_create_func.request_window("app@exit")
            func.print_log("接口返回：", [state, msg])
            if state == 1:
                try:
                    sleep(1)
                    icon.stop()
                except:
                    main_pid = os.getpid()
                    watch_processes.kill_process_by_pid(main_pid)
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
            watch_processes.kill_process_by_pid(main_pid)
            pass
        pass

    # 图标
    @staticmethod
    def load_icon(icon_binary):
        # 适用图片文件
        # _img = get_config("pytray", "icon")
        # if os.path.exists(_img): # mac/linux .png, win .ico
        #     image = Image.open(_img)
        #     return image.resize((64, 64), Image.Resampling.LANCZOS)
        # else:
        #     # 创建默认图标
        #     image = Image.new('RGB', (64, 64), 'blue')
        #     return image

        # 图片转成二进制
        # with open(_img, "rb") as f:
        #     icon_binary = f.read()

        # 使用 BytesIO 将二进制数据转换为图像（win、mac、linux均可使用）
        image = Image.open(io.BytesIO(icon_binary))
        # 确保图像尺寸合适（推荐 16x16, 32x32, 64x64, 128x128）
        image = image.resize((128, 128), Image.Resampling.LANCZOS)
        return image

    #
    pass


# 创建tray
# mac、win、linux创建时都会调用此函数，但不会被window.py直接调用
def tray_create():
    global CONFIG
    CONFIG = get_config("", "")

    # 选择性禁用“SSL报错”
    warnings.filterwarnings('ignore', message='Unverified HTTPS request', category=urllib3.exceptions.InsecureRequestWarning)

    # 创建菜单
    menu = pystray.Menu(
        pystray.MenuItem(text="" + func.get_translate("show_window"), action=tray_create_func.on_show_or_hide, default=True),
        pystray.Menu.SEPARATOR,
        # pystray.MenuItem(text="❗️ 关于"+CONFIG["app"]["app_name"], action=on_about, default=False),
        # pystray.Menu.SEPARATOR,
        pystray.MenuItem(text="🔴 " + func.get_translate("exit_app"), action=tray_create_func.on_exit, radio=False, default=False)
    )

    # 创建托盘图标
    icon = pystray.Icon(
        name=CONFIG["app"]["app_name"],  # app_name
        icon=tray_create_func.load_icon(ICON_Binary),  # 图标
        title="" + CONFIG["app"]["app_name"],  # hover tips
        menu=menu  # 菜单
    )

    # 创建线程
    t1 = threading.Thread(target=tray_create_func.tray_ping_window, daemon=True)

    # 启动线程
    t1.start()

    # 托盘
    icon.run()

    # 等待线程结束
    t1.join()

    pass
