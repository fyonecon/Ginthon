import webview
import psutil
import os
import threading

from internal.bootstrap.run_services import run_services
from internal.bootstrap.run_flask import run_flask
from internal.bootstrap.run_tray import run_tray
from internal.config import get_config
from internal.common.func import print_log, get_platform
from internal.common.app_auth import make_auth, make_rand_id
from internal.app.window.controller.on_events import on_closed,on_closing,on_shown,on_loaded,on_minimized,on_maximized,on_restored,on_resized,on_moved,on_before_load,on_before_show,on_initialized

#
CONFIG = {}
WINDOW = None
WEBVIEW_PID = None
SERVICES_PID = None
FLASK_PID = None


# 视窗view-url
def view_url(view_class=""):

    if view_class == "vue" or view_class == "svelte":
        # svelte dist 或 vue dist
        view_host = CONFIG["pywebview"]["view_host"]
        view_index_html = CONFIG["pywebview"]["view_index.html"]
        url = view_host + ":" + str(CONFIG["flask"]["port"]) + "/view" + view_index_html
        return url
    else:
        # 单页HTML
        view_host = CONFIG["pywebview"]["view_host"]
        rand_id = make_rand_id(CONFIG)
        view_auth = make_auth(CONFIG)
        url = view_host+":"+str(CONFIG["flask"]["port"])+ "/view/" + rand_id + "?" + "view_auth=" + view_auth + "&version=" + CONFIG["app"]["app_version"] + "&ap=" + CONFIG["app"][ "app_name"]
        return url


# 注册服务
def join_events(_window):
    global SERVICES_PID
    global FLASK_PID

    print("### Join ", "Process")

    # 创建线程
    t1 = threading.Thread(target=run_flask, daemon=True, args=(_window, WEBVIEW_PID, CONFIG))
    t2 = threading.Thread(target=run_services, daemon=True, args=(_window, WEBVIEW_PID, CONFIG))
    t3 = threading.Thread(target=run_tray, daemon=True, args=(_window, WEBVIEW_PID, CONFIG))

    # 启动线程
    t1.start()
    t2.start()
    t3.start()

    # 获取pid
    # SERVICES_PID = t1.pid
    # FLASK_PID = t2.pid

    # 等待线程结束
    t1.join()
    t2.join()
    t3.join()

    return


# 视窗（pywebview必须运行在主线程上）
def init_window(cmd_model):
    global CONFIG
    global WINDOW
    global WEBVIEW_PID
    global SERVICES_PID
    global FLASK_PID
    #
    CONFIG = get_config("", "")
    #
    _view_url = view_url(CONFIG["pywebview"]["view_class"]) # 生产环境url：vue svelte ""
    _dev_url = CONFIG["pywebview"]["dev_url"] # 开发环境url
    if cmd_model == "dev":
        pywebveiw_url = _dev_url
        pass
    else:
        cmd_model = "build"
        pywebveiw_url = _view_url
        pass
    # 创建视窗
    _window = webview.create_window(
        title=CONFIG["app"]["app_name"],
        url=pywebveiw_url,
        # html='<h2>Ginthon</h2>',
        min_size=(520, 520),
        width=960, height=700, # width=720, height=540     width=960, height=700
        hidden=False, # 打开时隐藏界面，默认 False
        frameless=False, # 默认 False 拖住class="pywebview-drag-region"
        confirm_close=False, # 关闭window时显示确认窗口（不支持在状态栏关闭时拦截） False True
        text_select=True, # False True
        transparent=False,
        background_color="#505050",
        draggable=False, # 可以将图片拖到桌面，建议False
    )
    WINDOW = _window
    WEBVIEW_PID = os.getpid()
    print_log("### 视窗 => ", pywebveiw_url)

    # 窗口实时事件
    _window.events.closing += on_closing
    _window.events.shown += on_shown
    _window.events.loaded += on_loaded
    _window.events.minimized += on_minimized
    # _window.events.hidden += on_hidden
    _window.events.maximized += on_maximized
    _window.events.restored += on_restored
    _window.events.resized += on_resized
    _window.events.moved += on_moved
    _window.events.before_load += on_before_load
    _window.events.before_show += on_before_show
    _window.events.initialized += on_initialized
    _window.events.closed += on_closed

    # 启动视窗
    webview.start(func=join_events, args=_window, ssl=CONFIG["pywebview"]["ssl"], debug=CONFIG["pywebview"]["debug"], user_agent="webview2_webkit_desktop/gthon_v"+CONFIG["app"]["app_version"]+"/"+get_platform()+"_"+cmd_model+"(fy_ginthon)")

    # 主动杀掉join_events服务进程
    try:
        print("主动杀剩余进程：", [SERVICES_PID, FLASK_PID])
        process_services = psutil.Process(SERVICES_PID)
        process_services.kill()
        process_flask = psutil.Process(FLASK_PID)
        process_flask.kill()
        pass
    except Exception:
        print("XXX 不存在的PID：", [SERVICES_PID, FLASK_PID])
        pass

    #
    print("===视窗服务已经结束===", [WEBVIEW_PID, SERVICES_PID, FLASK_PID])
    #
    return
