import os

from flask import send_file, request

from internal.app.flask.controller.window_view import window_view
from internal.common.func import back_404_data_api, back_404_data_html, get_file_ext_mimetype, get_file_ext, \
    back_404_data_file, has_file
from internal.common.main_dirpath import mian_virtual_dirpath
from internal.common.view_auth import check_rand_id, check_rand_token
from internal.common.watch_pid import kill_process_by_pid
from internal.config import get_config


# 自定义路由，html模板
def custom_routes_html(FLASK, flask_middleware_html):

    # 视窗专用 http://127.0.0.1:9100/window/xxx
    @FLASK.route("/window/<rand_id>", methods=["GET"])
    def window(rand_id, filename="index.html"):
        # print("method2=", request.method, request.headers, request.url)
        route_data = {
            "way": "html",
            "methods": ["GET"],
        }
        rand_id_state = check_rand_id(rand_id)
        if rand_id_state: # 正确
            html_data = window_view(rand_id, filename)
            response_data, reg_code = flask_middleware_html(request, route_data, html_data, filename)
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
        #
        if tray_rand_token_state:  # 正确
            #####################################
            if do == "app@show_or_hide":
                state = 1
                msg = "show"
                window.show()
                pass
            #####################################
            elif do == "app@about":
                state = 1
                msg = "about"
                #
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

        #
        back_data = {
            "state": state,  #
            "msg": msg,
            "content": {
                # "tray_rand_token": tray_rand_token,
                "view_auth": view_auth,
                "do": do,
                "app_class": app_class,
            }
        }
        response_data, reg_code = flask_middleware_api(request, route_data, back_data, "")
        if reg_code == 200:
            return response_data, reg_code
        else:
            return back_404_data_api("非法操作"), reg_code
    # api
    pass


# 自定义路由，文件专用
def custom_routes_file(FLASK, flask_middleware_file):

    # 主file的资源。 http://127.0.0.1:9100/file/test.txt
    @FLASK.route("/file/<path:filename>", methods=["GET", "POST", "OPTIONS"])
    def file(filename):  # filename可以包含路径
        route_data = {
            "way": "file",
            "methods": ["GET"],
        }
        file_ext = get_file_ext(filename)
        mimetype = get_file_ext_mimetype(file_ext)
        file_path = mian_virtual_dirpath("frontend") + "/file" + "/" + filename # 限定根目录
        if has_file(file_path):
            response_data, reg_code = flask_middleware_file(request, route_data, "", filename)
            if reg_code == 200:
                # 使用返回文件的方式返回html模板或文件
                return send_file(file_path, as_attachment=False, mimetype=mimetype, max_age=12 * 60, download_name=filename), reg_code
            else:
                return back_404_data_file("非法操作"), reg_code
        else:
            return back_404_data_file("无对应文件：" + filename), 404

    # file
    pass

    # 主view-file的资源。
    # http://127.0.0.1:9100/view
    # http://127.0.0.1:9100/view/static/2.png
    @FLASK.route("/view/", methods=["GET"])
    @FLASK.route("/view", methods=["GET"])
    @FLASK.route("/view/<path:filename>", methods=["GET", "POST", "OPTIONS"])
    def frontend_files(filename=""): # filename可以包含路径
        route_data = {
            "way": "file",
            "methods": ["GET"],
        }
        if len(filename)==0:
            filename = "index.html"
            pass
        #
        file_ext = get_file_ext(filename)
        mimetype = get_file_ext_mimetype(file_ext)
        file_path = mian_virtual_dirpath("frontend") + "/view" + "/" + filename  # 限定根目录
        if has_file(file_path):
            response_data, reg_code = flask_middleware_file(request, route_data, "", filename)
            if reg_code == 200:
                # 使用返回文件的方式返回html模板或文件
                return send_file(file_path, as_attachment=False, mimetype=mimetype, max_age=12 * 60, download_name=filename), reg_code
            else:
                return back_404_data_file("非法操作"), reg_code
        else:
            return back_404_data_file("无对应文件：" + filename), 404

    # file
    pass
