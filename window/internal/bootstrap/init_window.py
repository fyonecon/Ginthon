import webview
import multiprocessing
import psutil
import os
import threading

from internal.bootstrap.run_services import run_services
from internal.bootstrap.run_flask import run_flask
from internal.config import get_config
from internal.common.func import print_log, get_platform
from internal.common.view_auth import make_view_auth, make_view_rand_id
# from internal.app.pywebview.window_events import on_closed,on_closing,on_shown,on_loaded,on_minimized,on_maximized,on_restored,on_resized,on_moved,on_before_load,on_before_show,on_initialized
# from internal.bootstrap.run0 import view_init, view_closed

#
CONFIG = {}
WINDOW = None
WEBVIEW_PID = None
SERVICES_PID = None
FLASK_PID = None

# 视窗view-url
def view_url():
    url = CONFIG["pywebview"]["url"]
    view_rand_id = make_view_rand_id(url, CONFIG)
    view_auth = make_view_auth(url, CONFIG)
    url = url+ "/" + view_rand_id + "?" + "view_auth=" + view_auth + "&version=" + CONFIG["app"]["app_version"] + "&ap=" + CONFIG["app"][ "app_name"]
    #
    return url

# 视窗view-html
def view_html(URL):
    #
    html1 = r'''
    <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0, user-scalable=0" />
            <title>Loading...</title>
            <style>
                html {
                    background-color: rgba(115,115,115,0.2);
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
        </head>
        <body>
            <div id="url-msg" class="url-msg select-none break click"></div>
            <script>
                const URL = "'''
    #
    html2 = r'''";
                let click_waiting = 0;
                let click_waiting_timeout = 0;
                // 是否是正确格式的url
                function isURLWithProtocols(str) {
                    const protocols = ['http', 'https', 'ftp', 'ftps', 'mailto', 'tel', 'sms'];
                    const protocolPattern = new RegExp(
                        `^(${protocols.join('|')}):\\/\\/[^\\s/$.?#].[^\\s]*$`,
                        'i'
                    );
                    return protocolPattern.test(str);
                }
                // 使用fetch检测网址是否可用
                async function pingURL(url, timeout = 6000) {
                    if (isURLWithProtocols(url)){
                        try {
                            // 添加时间戳避免缓存
                            const testUrl = url + (url.includes('?') ? '&' : '?') + '_t=' + Date.now();
                            const controller = new AbortController();
                            const timeoutId = setTimeout(() => controller.abort(), timeout);
                            const response = await fetch(testUrl, {
                                method: 'HEAD', // 使用HEAD方法，只请求头部信息
                                mode: 'no-cors', // 对于跨域请求，使用no-cors模式
                                signal: controller.signal
                            });
                            clearTimeout(timeoutId);
                            // 如果使用no-cors，response.status会是0，我们只关心是否成功连接
                            return response.ok || response.type === 'opaque';
                        } catch (error) {
                            console.log(`Ping失败: ${error.message}`);
                            return false;
                        }
                    }else{
                        return false
                    }
                }
                // 使用
                function load_url(_URL){
                    click_waiting = 1;
                    pingURL(_URL).then(state => {
                        let url = _URL.length>10?_URL:"(Services is null)";
                        console.log("URL状态：", [state, url]);
                        if (state){
                            document.getElementById("url-msg").innerHTML = "Services Loading....";
                            window.location.replace(url);
                        }else{
                            click_waiting_timeout = setTimeout(function (){
                                click_waiting = 0;
                                click_waiting_timeout = 0;
                                console.log("click waited.");
                            }, 2000);
                            document.getElementById("url-msg").innerHTML = "Services Timeout.";
                        }
                    });
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
    html3 =  html1+URL+html2
    print_log(html3)
    return html3

# 注册服务
def join_events(_window):
    global SERVICES_PID
    global FLASK_PID

    print("✅ Join ", "Process")

    # 创建线程
    t1 = threading.Thread(target=run_services, daemon=True)
    t2 = threading.Thread(target=run_flask, daemon=True)


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

    # sleep(2)

    # 创建进程（pywebview中创建multiprocessing会触发无限webview启动，必须是主线程）
    process_services = multiprocessing.Process(target=run_services)
    process_flask = multiprocessing.Process(target=run_flask)

    # 启动进程
    process_services.start()
    process_flask.start()

    # 获取pid
    SERVICES_PID = process_services.pid
    FLASK_PID = process_flask.pid

    # 等待进程完成
    process_services.join()
    process_flask.join()

    return

# 视窗
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
        # url=_view_url,
        html=_view_html,
        min_size=(520, 520),
        width=720, height=540,
        hidden=False,
        frameless=False,
        text_select=True,
        transparent=False,
        background_color="#555555",
    )
    WINDOW = _window
    WEBVIEW_PID = os.getpid()
    print_log("✅ 视窗 => ", _view_url)

    #
    # _window.events.initialized += view_init
    # _window.events.closed += view_closed
    # 其它
    # _window.events.closing += on_closing
    # _window.events.shown += on_shown
    # _window.events.loaded += on_loaded
    # _window.events.minimized += on_minimized
    # _window.events.maximized += on_maximized
    # _window.events.restored += on_restored
    # _window.events.resized += on_resized
    # _window.events.moved += on_moved
    # _window.events.before_load += on_before_load
    # _window.events.before_show += on_before_show

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
        print("❌ 不存在的PID：", [SERVICES_PID, FLASK_PID])
        pass

    #
    print("===视窗服务已经结束===", [WEBVIEW_PID, SERVICES_PID, FLASK_PID])
    #
    return
