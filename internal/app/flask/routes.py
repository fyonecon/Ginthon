import os

from flask import send_file, request

from internal.common.func import back_404_data_api, back_404_data_html
from internal.common.view_auth import check_rand_id, check_rand_token
from internal.common.watch_pid import kill_process_by_pid
from internal.config import get_config


# 自定义路由，视图专用
def custom_routes_html(FLASK, flask_middleware_html):

    # 视窗专用 http://127.0.0.1:9100/html/view/xxx
    @FLASK.route("/html/view/<rand_id>", methods=["GET", "POST", "OPTIONS"])
    def view(rand_id):
        # print("method2=", request.method, request.headers, request.url)
        route_data = {
            "way": "html",
            "methods": ["GET"],
        }
        rand_id_state = check_rand_id(rand_id)
        if rand_id_state: # 正确
            html_data = '''
                视窗已启动。
            '''
            response_data, reg_code = flask_middleware_html(request, route_data, html_data)
            if reg_code == 200:
                return response_data, reg_code
            else:
                return back_404_data_html("非法操作"), reg_code
        else: # 非法ID
            return back_404_data_html("非法ID"), 404

    # html
    pass


# 自定义路由，接口专用
def custom_routes_api(FLASK, flask_middleware_api, window):

    # 状态栏托盘专用 http://127.0.0.1:9100/api/tray/xxx
    @FLASK.route("/api/tray/<tray_rand_token>", methods=["GET", "POST", "OPTIONS"])  # 路由名
    def tray(tray_rand_token):  # 触发函数（函数名尽量和路由名一致）
        # print("method2=", tray_rand_token, request.method, request.headers, request.url)
        route_data = {
            "way": "json",
            "methods": ["POST", "OPTIONS"],
        }
        # 处理接收的数据
        data = request.get_json()
        if not data:
            return back_404_data_api("空的请求参数")

        #
        view_auth = data["view_auth"]
        do = data["do"]
        app_class = data["app_class"]
        salt_str = "pystray2025"
        CONFIG = get_config("tray")
        tray_rand_token_state, msg = check_rand_token(app_class, salt_str, CONFIG, tray_rand_token)
        #
        window_show_hide_state = "" # 视窗当前是否显示，需要从本地视窗获取状态（待定） “” show hide
        SHOW_HIDE_STATE = ""  # 无用或向托盘图标指示 “” show hide
        #
        if window_show_hide_state == "hide" and (do == "app@show" or do == "app@hide"): # 以视窗为准指示显示还是隐藏
            SHOW_HIDE_STATE = "show"
            window.show()
            pass
        elif window_show_hide_state == "show"and (do == "app@show" or do == "app@hide"): # 以视窗为准指示显示还是隐藏
            SHOW_HIDE_STATE = "hide"
            window.hide()
            pass
        else: # 以托盘图标为准指示视窗显示与隐藏
            if tray_rand_token_state:  # 正确
                #####################################
                if do == "app@show":
                    state = 1
                    msg = "show"
                    SHOW_HIDE_STATE = "show"
                    window.show()
                    pass
                elif do == "app@hide":
                    state = 1
                    msg = "hide"
                    SHOW_HIDE_STATE = "hide"
                    window.hide()
                    pass
                #####################################
                elif do == "app@about":
                    state = 1
                    msg = "about"
                    pass
                elif do == "app@exit":  # exit
                    state = 1
                    msg = "exit"
                    # 杀掉主程序（全部程序）
                    main_pid = os.getpid()
                    kill_process_by_pid(main_pid)
                    #
                    pass
                #####################################
                else:  # 未知状态
                    state = 0
                    msg = "未知状态：" + do
                    pass
                pass
            else:
                state = 0
                pass
            pass

        #
        back_data = {
            "state": state,  #
            "msg": msg,
            "content": {
                "SHOW_HIDE_STATE": SHOW_HIDE_STATE, # show hide
                "tray_rand_token": tray_rand_token,
                "view_auth": view_auth,
                "do": do,
                "app_class": app_class,
            }
        }
        response_data, reg_code = flask_middleware_api(request, route_data, back_data)
        if reg_code == 200:
            return response_data, reg_code
        else:
            return back_404_data_api("非法操作"), reg_code

    # api
    pass


# 自定义路由，文件专用
def custom_routes_file(FLASK, flask_middleware_file):
    #
    @FLASK.route("/file/<filename>", methods=["GET", "POST", "OPTIONS"])  # 路由名
    def file(filename):  # 触发函数（函数名尽量和路由名一致）
        filetype = ""
        # flask_response("file", status_code=200, filename=filename, filetype=filetype)
        file_path = 'xx/xx.pdf'
        return send_file(file_path, as_attachment=True)

    # file
    pass