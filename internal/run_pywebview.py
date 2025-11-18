import webview

from common.config import get_config
from common.view_auth import make_view_auth

#
CONFIG = {}

# 启动客户端
def run_pywebview():
    #
    global CONFIG
    CONFIG = get_config("run_pywebview")
    #
    url = "http://127.0.0.1:"+str(CONFIG["flask"]["port"])
    view_auth = make_view_auth(url, CONFIG)
    print("✅ 视窗服务 => ", "URL=" + url)
    #
    webview.create_window(CONFIG["app"]["app_name"], url+"?view_auth="+view_auth+"&version="+CONFIG["app"]["app_version"]+"&ap="+CONFIG["app"]["app_name"])
    webview.start(ssl=CONFIG["pywebview"]["ssl"], debug=CONFIG["pywebview"]["debug"])
    pass
