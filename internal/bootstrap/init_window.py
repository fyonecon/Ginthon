import webview
import multiprocessing
import psutil
import os
import threading

from internal.bootstrap.run_services import run_services
from internal.bootstrap.run_flask import run_flask
from internal.config import get_config
from internal.common.func import print_log
from internal.bootstrap.app_auth import make_auth, make_rand_id
from internal.app.window.controller.on_events import on_closed,on_closing,on_shown,on_loaded,on_minimized,on_maximized,on_restored,on_resized,on_moved,on_before_load,on_before_show,on_initialized

#
CONFIG = {}
WINDOW = None
WEBVIEW_PID = None
SERVICES_PID = None
FLASK_PID = None


# 视窗view-url
def view_url():
    view_host = CONFIG["pywebview"]["view_host"]
    rand_id = make_rand_id(CONFIG)
    view_auth = make_auth(CONFIG)
    url = view_host+":"+str(CONFIG["flask"]["port"])+ "/window/" + rand_id + "?" + "view_auth=" + view_auth + "&version=" + CONFIG["app"]["app_version"] + "&ap=" + CONFIG["app"][ "app_name"]
    #
    return url


# 视窗view-html
def view_html(URL):
    html1 = f'''
    <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0, user-scalable=0" />
            <link rel="apple-touch-icon" href="/launcher.png">
            <link rel="shortcut icon" href="/favicon.ico" type="image/x-icon" />
            <title>Loading...</title>
            <script>
                const URL = "{URL}";
            </script>'''

    html2 = '''
        </head>
        <body>
            <style>
                html {
                    background-color: rgba(115,115,115,0.8);
                }
                body {
                    background-color: transparent;
                    padding: 0 0;
                    margin: 0 0;
                }
                .hide{
                    display: none !important;
                }
                .click{
                    cursor: pointer;
                }
                .click:active{
                    opacity: 0.6;
                }
                .select-none{
                    -moz-user-select: none;-webkit-user-select: none;-ms-user-select: none;
                    user-select: none;
                }
                .break{
                    overflow: hidden;
                    word-wrap: break-word;
                    overflow-wrap: break-word;
                }
                .url-msg{
                    font-size: 18px;
                    line-height: 30px;
                    text-align: center;
                    padding: 20px 10px;
                }
            </style>
            <div id="url-msg" class="url-msg select-none break click">Default View.</div>
            <script>
                let click_waiting = 0;
                let click_waiting_timeout = 0;
                // 使用
                function load_url(_URL){
                    click_waiting = 1;
                    click_waiting_timeout = 1;
                    //
                    if (_URL.length >= 9){
                        document.getElementById("url-msg").innerHTML = "Services Loading....";
                        //
                        window.location.replace(_URL);
                    }else{
                        click_waiting = 0;
                        click_waiting_timeout = 0;
                        document.getElementById("url-msg").innerHTML = "URL Error.";
                    }
                }
                (function (){
                    load_url(URL);
                })();
                document.getElementById("url-msg").onclick = function (){
                    if (click_waiting === 0 && click_waiting_timeout === 0){ // 防止连续点击
                        load_url(URL);
                    }else{
                        console.log("click waiting...", [click_waiting, click_waiting_timeout]);
                    }
                };
            </script>
        </body>
        </html>
    '''
    #
    html3 = html1+html2
    print_log(html3)
    return html3


# 注册服务
def join_events(_window):
    global SERVICES_PID
    global FLASK_PID

    print("### Join ", "Process")

    # 创建线程
    t1 = threading.Thread(target=run_services, daemon=True, args=(_window, WEBVIEW_PID, CONFIG))
    t2 = threading.Thread(target=run_flask, daemon=True, args=(_window, WEBVIEW_PID, CONFIG))


    # 启动线程
    t1.start()
    t2.start()

    # 获取pid
    # SERVICES_PID = t1.pid
    # FLASK_PID = t2.pid

    # 等待线程结束
    t1.join()
    t2.join()

    return


# 视窗（pywebview必须运行在主线程上）
def init_window():
    global CONFIG
    global WINDOW
    global WEBVIEW_PID
    global SERVICES_PID
    global FLASK_PID
    #
    CONFIG = get_config("run_pywebview")
    _view_url = view_url()
    _view_html = view_html(_view_url)

    # 创建视窗
    _window = webview.create_window(
        title=CONFIG["app"]["app_name"],
        url=_view_url,
        # html=_view_html,
        min_size=(520, 520),
        width=720, height=540,
        hidden=True, # 打开时隐藏界面，默认 False
        frameless=False,
        text_select=True,
        transparent=False,
        background_color="#555555",
    )
    WINDOW = _window
    WEBVIEW_PID = os.getpid()
    print_log("### 视窗 => ", _view_url)

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
    webview.start(func=join_events, args=_window, ssl=CONFIG["pywebview"]["ssl"], debug=CONFIG["pywebview"]["debug"])

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
