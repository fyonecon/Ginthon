import requests

from internal.common.view_auth import make_view_rand_id, make_view_auth
from internal.config import get_config


# 请求window视图的状态
def request_window(do):
    CONFIG = get_config()

    #
    tray_rand_id = make_view_rand_id("", CONFIG)

    # API
    url = CONFIG["pywebview"]["url"]+"/"+tray_rand_id
    # 请求数据
    payload = {
        "app_class": CONFIG["app"]["app_class"],
        "do": do,
        "view_auth": make_view_auth("", CONFIG)
    }
    # 请求头
    headers = {
        "Content-Type": "application/json",
        "User-Agent": CONFIG["app"]["app_name"]+"/"+CONFIG["app"]["app_version"],
    }
    print("请求：", url)
    # 发送POST
    response = requests.post(
        url,
        json=payload,
        headers=headers,
        timeout=3  # 超时设置，s
    )
    # 返回信息
    if response.status_code == 200: # 200
        res = response.json()
        state = res["json"]["state"]
        msg = res["json"]["msg"]
        return state, msg
    else: # 其它情况
        return 404, "接口请求错误：" + str(response.status_code)
    pass

# 托盘菜单操作
# 1 show， 0 hide
def on_show_or_hide(icon, item_text):
    state, msg = request_window("app@show_or_hide")
    print("接口返回：", [state, msg])
    if state == 1:
        #
        pass
    else:
        icon.notify(title="未知状态："+str(state), message=msg)
        pass
    pass
    pass

# 关于
# 1 成功
def on_about(icon, item_text):
    state, msg = request_window("app@about")
    print("接口返回：", [state, msg])
    if state == 1:
        #
        pass
    else:
        icon.notify(title="未知状态：" + str(state), message=msg)
        pass
    pass

# 退出程序
# 1 exit
def on_exit(icon, item):
    state, msg = request_window("app@exit")
    print("接口返回：", [state, msg])
    if state == 1:
        icon.stop()
        #
        pass
    else:
        icon.notify(title="未知状态："+str(state), message=msg)
        pass
    pass