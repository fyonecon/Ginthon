from flask import request, send_file

from internal.services.flask_middleware import flask_middleware_html, flask_middleware_file, flask_middleware_api
from internal.common.func import func
from internal.common.kits.main_dirpath import main_dirpath
from internal.common.request_data import request_data


# 必要路由
# 请求宽进严出、中间件验证参数
def route_must(window, FLASK):

    # index http://127.0.0.1:9750/
    @FLASK.route("/", methods=["GET", "POST", "OPTIONS"]) # 路由名
    def index(filename="virtual.html"): # 触发函数（函数名尽量和路由名一致）
        # route验证参数
        route_data = {
            "way": "html", # 当前接口请求的数据请求的类型：html、json、file
            "methods": ["GET", "POST", "OPTIONS"], # 可接受的请求方法：["GET", "POST", "OPTIONS"]
        }

        # 接口接收的数据
        _test = request_data.input(request, "test")
        if _test is None:
            _test = "Null"
            pass

        # 返回的数据
        html_data = '''
            <html>
            <head>
            <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0, user-scalable=0" />
            <link rel="apple-touch-icon" href="/icon.png">
            <link rel="shortcut icon" href="/favicon.ico" type="image/x-icon" />
            <title>HTML is OK</title>
            <style>
                html {
                    background-color: rgba(115,115,115,0.4);
                }
                body {
                    background-color: transparent;
                    padding: 0 0;
                    margin: 10px 10px;
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
            </style>
            </head>
            <body><p id="info" class="break select-none">YES</p><p>test='''+_test+'''</p><script>function show_info() {let info = [window.location.host, !!window.localStorage, !!window.indexedDB, navigator.webdriver, navigator.languages, window.matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light", "✅", window.navigator.userAgent]; document.getElementById("info").innerHTML = info; console.log(info);}show_info();</script></body></html>
        '''
        # 用中间件验证参数
        response_data, reg_code = flask_middleware_html(request, route_data, html_data, filename)
        if reg_code == 200:
            return response_data, reg_code
        else:
            return func.back_404_data_html("非法操作:index"), reg_code


    # 图标
    @FLASK.route("/favicon.ico", methods=["GET", "POST", "OPTIONS"])
    def index_ico():  # filename可以包含路径
        route_data = {
            "way": "file",
            "methods": ["GET", "POST", "OPTIONS"],
        }
        filename = "favicon.ico"
        file_ext = func.get_file_ext(filename)
        mimetype = func.get_file_ext_mimetype(file_ext)
        file_path = main_dirpath.virtual_dirpath("frontend") + "/" + filename
        # 用中间件验证参数
        response_data, reg_code = flask_middleware_file(request, route_data, "", filename)
        if reg_code == 200:
            return send_file(file_path, as_attachment=False, mimetype=mimetype, max_age=12 * 60,
                             download_name=filename), reg_code
        else:
            return func.back_404_data_file("非法操作:white_file"), reg_code
        # ico图标

    # 图标
    @FLASK.route("/icon.png", methods=["GET", "POST", "OPTIONS"])
    def index_ico_png():  # filename可以包含路径
        route_data = {
            "way": "file",
            "methods": ["GET", "POST", "OPTIONS"],
        }
        filename = "icon.png"
        file_ext = func.get_file_ext(filename)
        mimetype = func.get_file_ext_mimetype(file_ext)
        file_path = main_dirpath.virtual_dirpath("frontend") + "/" + filename
        # 用中间件验证参数
        response_data, reg_code = flask_middleware_file(request, route_data, "", filename)
        if reg_code == 200:
            return send_file(file_path, as_attachment=False, mimetype=mimetype, max_age=12 * 60,
                             download_name=filename), reg_code
        else:
            return func.back_404_data_file("非法操作:white_file"), reg_code
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
        test = request_data.input(request, "test")

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
            return func.back_404_data_api("非法操作:api"), reg_code


    # 404
    @FLASK.errorhandler(404)
    def error_404(error):
        return func.back_404_data(), 404


    # 500
    @FLASK.errorhandler(500)
    def error_500(error):
        return func.back_500_data(), 500

    pass