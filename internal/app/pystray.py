from time import sleep

import requests
import os

from internal.common.func import print_log
from internal.bootstrap.app_auth import make_auth, make_rand_token
from internal.common.kits.watch_pid import kill_process_by_pid
from internal.config import get_config


# 请求window视图的状态
def request_window(do):
    CONFIG = get_config("", "")

    #
    app_class = CONFIG["app"]["app_class"]
    salt_str = "pystray2025"
    timeout_s = 2*365*24*60*60
    tray_rand_token = make_rand_token(app_class, salt_str, timeout_s, CONFIG)

    # API
    url = CONFIG["pywebview"]["url"]+"/"+tray_rand_token
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