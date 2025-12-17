# -*- coding: utf-8 -*-

from flask import send_file, request, redirect

from internal.app.window.controller.js_call_py import list_js_call_py
from internal.app.window.controller.tray_events import tray_events
from internal.app.window.window_view import view_js_must_data, view_index
from internal.common.app_auth import check_rand_id, check_rand_token
from internal.bootstrap.flask_middleware import flask_middleware_html, flask_middleware_api, flask_middleware_file
from internal.common.func import back_404_data_html, back_404_data_api, print_log, back_404_data_file, has_file, \
    get_file_ext_mimetype, get_file_ext, md5
from internal.common.kits.main_dirpath import mian_virtual_dirpath
from internal.config import get_config


# window专用路由
def window_route(_WINDOW, FLASK):

    # 适配svelte、vue文件结构的html静态文件系统
    # http://127.0.0.1:9750
    @FLASK.route("/", methods=["GET", "POST", "OPTIONS"])
    @FLASK.route("/<path:filename>", methods=["GET", "POST", "OPTIONS"])
    def svelte_dist(filename=""):
        route_data = {
            "way": "file",
            "methods": ["GET", "POST", "OPTIONS"],
        }
        #
        if len(filename) == 0:
            filename = "index.html"
            pass
        # 还原真实文件
        file_ext = get_file_ext(filename)
        if len(file_ext) == 0:  # 是路由就转成实际文件名
            filename = filename + ".html"
            pass
        config = get_config("", "")
        view_file_html = config["pywebview"]["view_file_html"] # "view/svelte/dist"、"view/vue/dist"
        file_ext = get_file_ext(filename)
        mimetype = get_file_ext_mimetype(file_ext)
        file_path = mian_virtual_dirpath("frontend") + "/" + view_file_html + "/" + filename  # 限定根目录
        #
        if has_file(file_path):
            response_data, reg_code = flask_middleware_file(request, route_data, "", filename)
            if reg_code == 200:
                # 使用返回文件的方式返回html模板或文件
                return send_file(file_path, as_attachment=False, mimetype=mimetype, max_age=12 * 60, download_name=filename), reg_code
            else:
                return back_404_data_file("非法操作：build。"+file_path), reg_code
        else:
            return back_404_data_file("无对应文件：" + filename), 404
    # file


    # view_js必要参数
    @FLASK.route("/js_must_data.js", methods=["GET", "POST", "OPTIONS"])
    def js_must_data(filename="js_must_data.js"):
        route_data = {
            "way": "file",
            "methods": ["GET", "POST", "OPTIONS"],
        }
        js_data = view_js_must_data()
        response_data, reg_code = flask_middleware_file(request, route_data, js_data, filename)
        if reg_code == 200:
            return response_data, reg_code
        else:
            return back_404_data_html("非法操作:must_data"), reg_code
    # file


    # 视窗单页型静态文件系统 http://127.0.0.1:9750/view/xxx
    @FLASK.route("/view/<rand_id>", methods=["GET", "POST", "OPTIONS"])
    def view(rand_id, filename="index.html"):
        route_data = {
            "way": "html",
            "methods": ["GET", "POST", "OPTIONS"],
        }
        rand_id_state = check_rand_id(rand_id)
        if rand_id_state:  # 正确
            html_data = view_index(_WINDOW, filename)
            #
            response_data, reg_code = flask_middleware_html(request, route_data, html_data, filename)
            if reg_code == 200:
                return response_data, reg_code
            else:
                return back_404_data_html("非法操作：view"), reg_code
        else:  # 非法ID
            return back_404_data_html("非法ID"), 404
    # html


    # 静态文件系统 http://127.0.0.1:9750/file/test.txt
    @FLASK.route("/file/<path:filename>", methods=["GET", "POST", "OPTIONS"])
    def file(filename):
        route_data = {
            "way": "file",
            "methods": ["GET", "POST", "OPTIONS"],
        }
        # 还原真实文件
        file_ext = get_file_ext(filename)
        if len(file_ext) >=1:  # 有文件
            file_ext = get_file_ext(filename)
            mimetype = get_file_ext_mimetype(file_ext)
            file_path = mian_virtual_dirpath("frontend") + "/file" + "/" + filename  # 限定根目录
            #
            if has_file(file_path):
                response_data, reg_code = flask_middleware_file(request, route_data, "", filename)
                if reg_code == 200:
                    # 使用返回文件的方式返回html模板或文件
                    return send_file(file_path, as_attachment=False, mimetype=mimetype, max_age=12 * 60,  download_name=filename), reg_code
                else:
                    return back_404_data_file("非法操作：file"), reg_code
            else:
                return back_404_data_file("无对应文件：" + filename), 404
        else:
            return back_404_data_file("无对应文件：" + filename), 404
    # file


    # js_call_py http://127.0.0.1:9750/api/js_call_py/xxx
    @FLASK.route("/api/js_call_py/<js_call_py_auth>", methods=["GET", "POST", "OPTIONS"])  # 路由名
    def js_call_py(js_call_py_auth):
        #
        route_data = {
            "way": "json",
            "methods": ["POST", "OPTIONS"],
        }
        # 处理接收的数据
        data = request.get_json()
        if not data:
            return back_404_data_api("空的请求参数")
        #
        config = get_config("", "")
        #
        app_class = config["app"]["app_class"]
        salt_str = "js_call_py_auth-2025"
        # 接收的参数
        _app_class = data["app_class"]
        _app_version = data["app_version"]
        _window_token = data["window_token"]
        _key = data["key"]
        _data_dict = data["data_dict"]
        #
        window_token_state = check_rand_id(_window_token)
        js_call_py_auth_state = check_rand_token(app_class, salt_str, config, js_call_py_auth)
        if js_call_py_auth_state and window_token_state:
            back_data = list_js_call_py(_WINDOW, key=_key, data_dict=_data_dict)
            #
            pass
        else:
            state = 0
            msg = "非法auth"
            back_data = {
                "state": state,  #
                "msg": msg,
                "content": data,
            }
            pass
        response_data, reg_code = flask_middleware_api(request, route_data, back_data, "")
        if reg_code == 200:
            return response_data, reg_code
        else:
            return back_404_data_api("非法操作:auth"), reg_code


    # 状态栏托盘专用 http://127.0.0.1:9750/api/tray/xxx
    @FLASK.route("/api/tray/<tray_rand_token>", methods=["GET", "POST", "OPTIONS"])  # 路由名
    def tray(tray_rand_token):  # 触发函数（函数名尽量和路由名一致）
        route_data = {
            "way": "json",
            "methods": ["POST", "OPTIONS"],
        }
        # 处理接收的数据
        data = request.get_json()
        if not data:
            return back_404_data_api("空的请求参数")
        #
        _app_class = data["app_class"]
        # _app_version = data["app_version"]
        # _app_token = data["app_token"]
        view_auth = data["view_auth"]
        do = data["do"]
        #
        salt_str = "pystray2025"
        CONFIG = get_config("", "")
        tray_rand_token_state, msg = check_rand_token(_app_class, salt_str, CONFIG, tray_rand_token)
        #
        if tray_rand_token_state:  # 正确
            state, msg = tray_events(_WINDOW, do)
            #
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
                "app_class": _app_class,
            }
        }
        response_data, reg_code = flask_middleware_api(request, route_data, back_data, "")
        if reg_code == 200:
            return response_data, reg_code
        else:
            return back_404_data_api("非法操作:tray"), reg_code

    #
    pass