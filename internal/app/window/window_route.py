from flask import send_file, request

from internal.app.window.controller.js_call_py import list_js_call_py
from internal.app.window.controller.tray_events import tray_events
from internal.app.window.window_view import window_view
from internal.bootstrap.app_auth import check_rand_id, check_rand_token
from internal.bootstrap.flask_middleware import flask_middleware_html, flask_middleware_api, flask_middleware_file
from internal.common.func import back_404_data_html, back_404_data_api, print_log, back_404_data_file, has_file, \
    get_file_ext_mimetype, get_file_ext
from internal.common.kits.main_dirpath import mian_virtual_dirpath
from internal.common.kits.watch_pid import kill_process_by_pid
from internal.config import get_config


#
def window_route(_WINDOW, FLASK):

    # 视窗专用 http://127.0.0.1:9100/window/xxx
    @FLASK.route("/window/<rand_id>", methods=["GET"])
    def window(rand_id, filename="index.html"):
        # print("method2=", request.method, request.headers, request.url)
        route_data = {
            "way": "html",
            "methods": ["GET"],
        }
        rand_id_state = check_rand_id(rand_id)
        if rand_id_state:  # 正确
            html_data = window_view(_WINDOW, rand_id, filename)
            response_data, reg_code = flask_middleware_html(request, route_data, html_data, filename)
            if reg_code == 200:
                return response_data, reg_code
            else:
                return back_404_data_html("非法操作"), reg_code
        else:  # 非法ID
            return back_404_data_html("非法ID"), 404
    # html


    # 主view-file的资源。
    # http://127.0.0.1:9100/view
    # http://127.0.0.1:9100/view/static/2.png
    @FLASK.route("/view/", methods=["GET"])
    @FLASK.route("/view", methods=["GET"])
    @FLASK.route("/view/<path:filename>", methods=["GET", "POST", "OPTIONS"])
    def frontend_files(filename=""):  # filename可以包含路径
        route_data = {
            "way": "file",
            "methods": ["GET"],
        }
        if len(filename) == 0:
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
                return send_file(file_path, as_attachment=False, mimetype=mimetype, max_age=12 * 60,
                                 download_name=filename), reg_code
            else:
                return back_404_data_file("非法操作"), reg_code
        else:
            return back_404_data_file("无对应文件：" + filename), 404


    # js_call_py http://127.0.0.1:9100/api/js_call_py/xxx
    @FLASK.route("/api/js_call_py/<js_call_py_auth>", methods=["GET", "POST", "OPTIONS"])  # 路由名
    def js_call_py(js_call_py_auth):
        route_data = {
            "way": "json",
            "methods": ["GET", "POST", "OPTIONS"],
        }
        # 处理接收的数据
        data = request.get_json()
        if not data:
            return back_404_data_api("空的请求参数")
        #
        config = get_config()
        #
        app_class = config["app"]["app_class"]
        salt_str = "js_call_py_auth-2025"
        #
        js_call_py_auth_state = check_rand_token(app_class, salt_str, config, js_call_py_auth)
        if js_call_py_auth_state:
            state = 1
            msg = "OK"
            pass
        else:
            state = 0
            msg = "非法auth"
            pass
        #
        back_data = {
            "state": state,  #
            "msg": msg,
            "content": data,
        }
        response_data, reg_code = flask_middleware_api(request, route_data, back_data, "")
        if reg_code == 200:
            #
            key = data["content"]["key"]
            data_dict = data["content"]["data_dict"]
            _state, _msg, _result = list_js_call_py(_WINDOW, config, key=key, data_dict=data_dict)
            # print("api=list_js_call_py=", [_state, _msg, key, data_dict, _result])
            result = {
                "state": _state,
                "msg": _msg,
                "content": {
                    "key": key,
                    "data_dict": data_dict,
                    "result": _result,
                },
            }
            return result, reg_code
        else:
            return back_404_data_api("非法操作"), reg_code


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
        if tray_rand_token_state:  # 正确
            state, msg = tray_events(_WINDOW, do)
            pass
        else:
            state = 0
            msg = "Token错误"
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
            #
            return response_data, reg_code
        else:
            return back_404_data_api("非法操作"), reg_code

    #
    pass