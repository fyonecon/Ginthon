# -*- coding: utf-8 -*-

from flask import send_file, request, redirect

from internal.app.app_window.controller.js_call_py import list_js_call_py
from internal.app.app_window.controller.tray_events import tray_events
from internal.app.app_window.window_view import view_js_must_data
from internal.common.app_auth import rand_id, rand_token
from internal.services.flask_middleware import flask_middleware_html, flask_middleware_api, flask_middleware_file
from internal.common.func import func
from internal.common.kits.main_dirpath import main_dirpath
from internal.config import get_config


# window专用路由
def route_window(_WINDOW, FLASK):

    # 适配svelte、vue文件结构的html静态文件系统。https://127.0.0.1:9750/view
    @FLASK.route("/view", methods=["GET", "POST", "OPTIONS"])
    @FLASK.route("/view/", methods=["GET", "POST", "OPTIONS"])
    def redirect_view():
        return redirect('/view/home')
    @FLASK.route("/view/<path:filename>", methods=["GET", "POST", "OPTIONS"], endpoint="view_dist")
    def view_dist(filename=""):
        #
        if len(filename) == 0:
            filename = "index.html"
            pass
        # 还原真实文件
        file_ext = func.get_file_ext(filename)
        if len(file_ext) == 0:  # 是路由就转成实际文件名
            filename = filename + ".html"
            pass
        file_ext = func.get_file_ext(filename)
        mimetype = func.get_file_ext_mimetype(file_ext)
        file_path = main_dirpath.virtual_dirpath("frontend") + "/view/dist/" + filename  # 限定根目录
        #
        if func.has_file(file_path):
            # 用中间件验证参数
            response_data, reg_code = flask_middleware_file(_request=request, _back_data="", _filename=filename)
            if reg_code == 200:
                # 使用返回文件的方式返回html模板或文件
                return send_file(file_path, as_attachment=False, mimetype=mimetype, max_age=12 * 60, download_name=filename), reg_code
            else:
                return func.back_404_data_file("非法操作：build。"+file_path), reg_code
        else:
            return func.back_404_data_file("无对应文件-vue/svelte：" + filename), 404
    # file


    # 提供可暴露在外的web静态文件访问。https://127.0.0.1:9750/html
    @FLASK.route("/html", methods=["GET", "POST", "OPTIONS"])
    @FLASK.route("/html/<path:filename>", methods=["GET", "POST", "OPTIONS"], endpoint="html")
    def html(filename=""):
        #
        if len(filename) == 0:
            filename = "index.html"
            pass
        # 还原真实文件
        file_ext = func.get_file_ext(filename)
        if len(file_ext) == 0:  # 是路由就转成实际文件名
            filename = filename + ".html"
            pass
        config = get_config("", "")
        file_ext = func.get_file_ext(filename)
        mimetype = func.get_file_ext_mimetype(file_ext)
        file_path = main_dirpath.virtual_dirpath("flaskassets") + "/html/" + filename  # 限定根目录
        #
        if func.has_file(file_path):
            # 用中间件验证参数
            response_data, reg_code = flask_middleware_file(_request=request, _back_data="", _filename=filename)
            if reg_code == 200:
                # 使用返回文件的方式返回html模板或文件
                return send_file(file_path, as_attachment=False, mimetype=mimetype, max_age=12 * 60,
                                 download_name=filename), reg_code
            else:
                return func.back_404_data_file("非法操作：html。" + file_path), reg_code
        else:
            return func.back_404_data_file("无对应文件-html：" + filename), 404
    # file


    # 其它可网络访问的文件。https://127.0.0.1:9750/files/test.txt
    @FLASK.route("/files", methods=["GET", "POST", "OPTIONS"])
    @FLASK.route("/files/<path:filename>", methods=["GET", "POST", "OPTIONS"])
    def file(filename):
        # 还原真实文件
        file_ext = func.get_file_ext(filename)
        if len(file_ext) >= 1:  # 有文件
            mimetype = func.get_file_ext_mimetype(file_ext)
            file_path = main_dirpath.virtual_dirpath("flaskassets") + "/files/" + filename  # 限定根目录
            #
            if func.has_file(file_path):
                # 用中间件验证参数
                response_data, reg_code = flask_middleware_file(_request=request, _back_data="", _filename=filename)
                if reg_code == 200:
                    # 使用返回文件的方式返回html模板或文件
                    return send_file(file_path, as_attachment=False, mimetype=mimetype, max_age=12 * 60,
                                     download_name=filename), reg_code
                else:
                    return func.back_404_data_file("非法操作：files"), reg_code
            else:
                return func.back_404_data_file("无对应文件-files：" + filename), 404
        else:
            return func.back_404_data_file("无对应文件-files：" + filename), 404
    # file


    # view_js必要参数
    @FLASK.route("/js_must_data.js", methods=["GET", "POST", "OPTIONS"])
    def js_must_data(filename="js_must_data.js"):
        back_data = view_js_must_data()

        # 用中间件验证参数
        response_data, reg_code = flask_middleware_file(_request=request, _back_data=back_data, _filename=filename)
        if reg_code == 200:
            return response_data, reg_code
        else:
            return func.back_404_data_html("非法操作:must_data"), reg_code
    # file


    # js_call_py http://127.0.0.1:9750/api/js_call_py/xxx
    @FLASK.route("/api/js_call_py/<js_call_py_auth>", methods=["GET", "POST", "OPTIONS"])  # 路由名
    def js_call_py(js_call_py_auth):
        # 处理接收的数据
        data = request.get_json()
        if not data:
            return func.back_404_data_api("空的请求参数")
        #
        config = get_config("", "")
        #
        app_class = config["app"]["app_class"]
        salt_str = "js_call_py_auth-2025"
        # 接收的参数
        _app_class = data["app_class"]
        _app_version = data["app_version"]
        _window_token = data["window_token"]
        # 检查必要参数
        if data.get("key"):
            _key = data["key"]
        else:
            _key = "test"
        if data.get("data_dict"):
            _data_dict = data["data_dict"]
        else:
            _data_dict = {}
        #
        window_token_state = rand_id.check(_window_token)
        js_call_py_auth_state = rand_token.check(app_class, salt_str, config, js_call_py_auth)
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

        # 用中间件验证参数
        response_data, reg_code = flask_middleware_api(_request=request, _back_data=back_data)
        if reg_code == 200:
            return response_data, reg_code
        else:
            return func.back_404_data_api("非法操作:auth"), reg_code


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
            return func.back_404_data_api("空的请求参数")
        #
        _app_class = data["app_class"]
        # _app_version = data["app_version"]
        # _app_token = data["app_token"]
        view_auth = data["view_auth"]
        do = data["do"]
        #
        salt_str = "pystray2025"
        CONFIG = get_config("", "")
        tray_rand_token_state, msg = rand_token.check(_app_class, salt_str, CONFIG, tray_rand_token)
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

        # 用中间件验证参数
        response_data, reg_code = flask_middleware_api(_request=request, _back_data=back_data)
        if reg_code == 200:
            return response_data, reg_code
        else:
            return func.back_404_data_api("非法操作:tray"), reg_code

    #
    pass