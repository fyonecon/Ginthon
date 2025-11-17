import webview

#
CONFIG = {}

# 启动客户端
def run_pywebview(config):
    #
    global CONFIG
    CONFIG = config
    #
    url = "http://127.0.0.1:"+str(CONFIG["flask"]["port"])
    print("✅ 视窗服务 => ", "URL=" + url)
    #
    webview.create_window(CONFIG["app_name"], url)
    webview.start()
    pass
