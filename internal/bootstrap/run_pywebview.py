import webview

from internal.common.config import get_config
from internal.common.func import main_path, has_file
from internal.common.view_auth import make_view_auth
from internal.app.pywebview.window_events import on_closed,on_closing,on_shown,on_loaded,on_minimized,on_maximized,on_restored,on_resized,on_moved,current_window,on_before_load,on_before_show,on_initialized

#
CONFIG = {}
WINDOW = None

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
    icon = CONFIG["sys"]["icon"]
    global WINDOW
    window = webview.create_window(
        title=CONFIG["app"]["app_name"],
        url=url+"?view_auth="+view_auth+"&version="+CONFIG["app"]["app_version"]+"&ap="+CONFIG["app"]["app_name"],
        # html=''' <p>200</p> ''',
        min_size=(520, 520),
        width=540, height=540,
        hidden=False,
        frameless=False,
        text_select=True,
        transparent=False,
        background_color="#333333",
    )
    WINDOW = window
    # 其它
    window.events.closed += on_closed
    window.events.closing += on_closing
    window.events.shown += on_shown
    window.events.loaded += on_loaded
    window.events.minimized += on_minimized
    window.events.maximized += on_maximized
    window.events.restored += on_restored
    window.events.resized += on_resized
    window.events.moved += on_moved
    window.events.before_load += on_before_load
    window.events.before_show += on_before_show
    window.events.initialized += on_initialized
    #
    webview.start(func=current_window, args=window, ssl=CONFIG["pywebview"]["ssl"], debug=CONFIG["pywebview"]["debug"], icon=icon)
    pass
