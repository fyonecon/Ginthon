import webview

from common.view_auth import make_view_auth

#
CONFIG = {}

# 启动客户端
def run_pywebview(config):
    #
    global CONFIG
    CONFIG = config
    #
    url = "http://127.0.0.1:"+str(CONFIG["flask"]["port"])
    view_auth = make_view_auth(url, CONFIG)
    print("✅ 视窗服务 => ", "URL=" + url)
    #
    webview.create_window(CONFIG["app_name"], url+"?view_auth="+view_auth+"&version="+CONFIG["app_version"]+"&ap="+CONFIG["app_name"])
    webview.start(ssl=CONFIG["pywebview"]["ssl"], debug=CONFIG["pywebview"]["debug"])
    pass
