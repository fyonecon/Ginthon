# -*- coding: utf-8 -*-

from flask import Flask, jsonify, send_file
from internal.app.flask.flask_route_api import flask_route_api
from internal.app.flask.flask_route_html import flask_route_html
from internal.app.flask.flask_route_file import flask_route_file
from flask import make_response, request

from internal.app.window.window_route import window_route
from internal.bootstrap.flask_middleware import flask_middleware_html, flask_middleware_file, flask_middleware_api
from internal.common.kits.main_dirpath import mian_virtual_dirpath
from internal.common.func import print_log, back_404_data, back_500_data, back_404_data_api, back_404_data_html, back_404_data_file, get_file_ext, get_file_ext_mimetype
from internal.common.request_input import request_input

#
CONFIG = {}

# 必要路由
# 请求宽进严出、中间件验证参数
def must_route(window, FLASK):

    # index http://127.0.0.1:9750/
    # @FLASK.route("/", methods=["GET", "POST", "OPTIONS"]) # 路由名
    # def index(filename="virtual.html"): # 触发函数（函数名尽量和路由名一致）
    #     # route验证参数
    #     route_data = {
    #         "way": "html", # 当前接口请求的数据请求的类型：html、json、file
    #         "methods": ["GET", "POST", "OPTIONS"], # 可接受的请求方法：["GET", "POST", "OPTIONS"]
    #     }
    #
    #     # 接口接收的数据
    #     if request.method == "GET":
    #         _test = request.args.get("test")
    #         if not _test:
    #             _test = "Null"
    #             pass
    #         pass
    #     elif request.method == "POST":
    #         try:
    #             data = request.get_json()
    #             if not data:
    #                 data = {"test": "NULL"}
    #                 pass
    #         except:
    #             data = {"test": "NULL"}
    #             pass
    #         _test = data["test"]
    #         pass
    #     else:
    #         return back_404_data_html("非法操作:index"), 404
    #
    #     # 返回的数据
    #     html_data = '''
    #         <html>
    #         <head>
    #         <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0, user-scalable=0" />
    #         <link rel="apple-touch-icon" href="/icon.png">
    #         <link rel="shortcut icon" href="/favicon.ico" type="image/x-icon" />
    #         <title>HTML is OK</title>
    #         <style>
    #             html {
    #                 background-color: rgba(115,115,115,0.4);
    #             }
    #             body {
    #                 background-color: transparent;
    #                 padding: 0 0;
    #                 margin: 10px 10px;
    #             }
    #             .hide{
    #                 display: none !important;
    #             }
    #             .click{
    #                 cursor: pointer;
    #             }
    #             .click:active{
    #                 opacity: 0.6;
    #             }
    #             .select-none{
    #                 -moz-user-select: none;-webkit-user-select: none;-ms-user-select: none;
    #                 user-select: none;
    #             }
    #             .break{
    #                 overflow: hidden;
    #                 word-wrap: break-word;
    #                 overflow-wrap: break-word;
    #             }
    #         </style>
    #         </head>
    #         <body><p id="info" class="break select-none">YES</p><p>test='''+_test+'''</p><script>function show_info() {let info = [window.location.host, !!window.localStorage, !!window.indexedDB, navigator.webdriver, navigator.languages, window.matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light", "✅", window.navigator.userAgent]; document.getElementById("info").innerHTML = info; console.log(info);}show_info();</script></body></html>
    #     '''
    #     # 用中间件验证参数
    #     response_data, reg_code = flask_middleware_html(request, route_data, html_data, filename)
    #     if reg_code == 200:
    #         return response_data, reg_code
    #     else:
    #         return back_404_data_html("非法操作:index"), reg_code


    # 图标
    @FLASK.route("/favicon.ico", methods=["GET", "POST", "OPTIONS"])
    def index_ico():  # filename可以包含路径
        route_data = {
            "way": "file",
            "methods": ["GET", "POST", "OPTIONS"],
        }
        filename = "favicon.ico"
        file_ext = get_file_ext(filename)
        mimetype = get_file_ext_mimetype(file_ext)
        file_path = mian_virtual_dirpath("frontend") + "/" + filename
        # 用中间件验证参数
        response_data, reg_code = flask_middleware_file(request, route_data, "", filename)
        if reg_code == 200:
            return send_file(file_path, as_attachment=False, mimetype=mimetype, max_age=12 * 60,
                             download_name=filename), reg_code
        else:
            return back_404_data_file("非法操作:white_file"), reg_code
        # ico图标

    # 图标
    @FLASK.route("/icon.png", methods=["GET", "POST", "OPTIONS"])
    def index_ico_png():  # filename可以包含路径
        route_data = {
            "way": "file",
            "methods": ["GET", "POST", "OPTIONS"],
        }
        filename = "icon.png"
        file_ext = get_file_ext(filename)
        mimetype = get_file_ext_mimetype(file_ext)
        file_path = mian_virtual_dirpath("frontend") + "/" + filename
        # 用中间件验证参数
        response_data, reg_code = flask_middleware_file(request, route_data, "", filename)
        if reg_code == 200:
            return send_file(file_path, as_attachment=False, mimetype=mimetype, max_age=12 * 60,
                             download_name=filename), reg_code
        else:
            return back_404_data_file("非法操作:white_file"), reg_code
        # ico图标


    # api http://127.0.0.1:9750/api
    #     # GET
    #     response = requests.get(url=url, timeout=12, headers=headers, params=data)
    #     print("response=", response.status_code, response.url, response.json())
    #
    #     # POST
    #     response = requests.post(url=url, timeout=12, headers=headers, json=data)
    #     print("response=", response.status_code, response.json())
    @FLASK.route("/api/", methods=["GET", "POST", "OPTIONS"])  # 路由名
    @FLASK.route("/api", methods=["GET", "POST", "OPTIONS"])  # 路由名
    def api():  # 触发函数（函数名尽量和路由名一致）
        # route验证参数
        route_data = {
            "way": "api", # 当前接口请求的数据请求的类型：html、api、file
            "methods": ["GET", "POST", "OPTIONS"], # 可接受的请求方法：["GET", "POST", "OPTIONS"]
        }

        # 接口接收的数据
        test = request_input(request, "test")

        # test
        if test is None:
            state = 1
            msg = "API is OK, but request data(test) is null."
            pass
        else:
            state = 1
            msg = "API is OK"
            pass

        # 返回的数据
        back_data = {
            "state": state,  # state=1代表有数据，state=0代表无数据或请求条件不足，但他们的status_code都是200。除此之外的state状态=status_code状态。
            "msg": msg,
            "content": {
                "test": test,
                "method": request.method,
                "url": request.url,
                "cookie": request.cookies,
            }
        }

        # 用中间件验证参数
        response_data, reg_code = flask_middleware_api(request, route_data, back_data, "")

        if reg_code == 200:
            return response_data, reg_code
        else:
            return back_404_data_api("非法操作:api"), reg_code


    # 404
    @FLASK.errorhandler(404)
    def error_404(error):
        return back_404_data(), 404


    # 500
    @FLASK.errorhandler(500)
    def error_500(error):
        return back_500_data(), 500

    pass


# 启动Flask服务
def run_flask(window, webview_pid, config):
    # 读取配置信息
    global CONFIG
    CONFIG = config
    #
    print_log("### Flask => ", "http://127.0.0.1" + ":" + str(CONFIG["flask"]["port"])+"/api")
    #
    FLASK = Flask(__name__)

    # 装饰器
    @FLASK.before_request
    def before_request():
        """全局处理 OPTIONS 请求"""
        if request.method == 'OPTIONS':
            response = jsonify()
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Requested-With')
            response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            return response
        else:
            return None

    # flask必要路由
    must_route(window, FLASK)
    # window必要路由
    window_route(window, FLASK)
    # 注册自定义路由
    flask_route_html(window, FLASK)
    flask_route_api(window, FLASK)
    flask_route_file(window, FLASK)
    #
    FLASK.run(debug=CONFIG["flask"]["debug"], port=CONFIG["flask"]["port"])

    # 检测端口在check_sys中，此处不再检测。

    pass