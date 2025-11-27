from flask import Flask, jsonify
from internal.app.flask.routes import custom_routes_html, custom_routes_api, custom_routes_file
from flask import make_response, request

from internal.config import get_config
from internal.common.func import print_log, back_404_data, back_500_data, back_404_data_api, back_404_data_html, back_404_data_file

#
CONFIG = {}

# 必要路由
# 请求宽进严出、中间件验证参数
def must_routes(FLASK):
    # index http://127.0.0.1:9100
    @FLASK.route("/", methods=["GET", "POST", "OPTIONS"]) # 路由名
    def index(): # 触发函数（函数名尽量和路由名一致）
        # route验证参数
        route_data = {
            "way": "html", # 当前接口请求的数据请求的类型：html、json、file
            "methods": ["GET", "HEAD", "POST", "OPTIONS"], # 可接受的请求方法：["GET", "POST", "OPTIONS"]
        }

        # 接口接收的数据
        if request.method == "GET":
            _test = request.args.get("test")
            if not _test:
                _test = None
                pass
            pass
        elif request.method == "POST":
            try:
                data = request.get_json()
                if not data:
                    data = {"test": None}
                    pass
            except:
                data = {"test": None}
                pass
            _test = data["test"]
            pass
        else:
            return back_404_data_html("非法操作"), 404

        # 返回的数据
        html_data = ''' 
            <html><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0, user-scalable=0" /><title>HTML is OK</title><body><p id="info" style="color:grey;">YES</p><p>test='''+_test+'''</p><script>function show_info() {let info = [window.location.host, !!window.localStorage, !!window.indexedDB, navigator.webdriver, navigator.languages, window.matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light", "###", window.navigator.userAgent]; document.getElementById("info").innerHTML = info; console.log(info);}show_info();</script></body></html>
        '''
        # 用中间件验证参数
        response_data, reg_code = flask_middleware_html(request, route_data, html_data)
        if reg_code == 200:
            return response_data, reg_code
        else:
            return back_404_data_html("非法操作"), reg_code

    # api http://127.0.0.1:9100/api
    #     # GET
    #     response = requests.get(url=url, timeout=12, headers=headers, params=data)
    #     print("response=", response.status_code, response.url, response.json())
    #
    #     # POST
    #     response = requests.post(url=url, timeout=12, headers=headers, json=data)
    #     print("response=", response.status_code, response.json())
    @FLASK.route("/api", methods=["GET", "POST", "OPTIONS"])  # 路由名
    def api():  # 触发函数（函数名尽量和路由名一致）
        # route验证参数
        route_data = {
            "way": "api", # 当前接口请求的数据请求的类型：html、api、file
            "methods": ["GET", "POST", "OPTIONS"], # 可接受的请求方法：["GET", "POST", "OPTIONS"]
        }

        # 接口接收的数据
        if request.method == "GET":
            _test = request.args.get("test")
            if not _test:
                data = {"test": None}
                pass
            else:
                data = {"test": _test}
                pass
            pass
        elif request.method == "POST":
            try:
                data = request.get_json()
                if not data:
                    data = {"test": None}
                    pass
            except:
                data = {"test": None}
                pass
            pass
        else:
            return back_404_data_api("非法操作"), 404

        # test
        if data["test"] is None:
            state = 1
            msg = "API is OK, but request data(test) is null."
            test = data["test"]
            pass
        else:
            state = 1
            msg = "API is OK"
            test = data["test"]
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
        response_data, reg_code = flask_middleware_api(request, route_data, back_data)

        if reg_code == 200:
            return response_data, reg_code
        else:
            return back_404_data_api("非法操作"), reg_code

    # 404
    @FLASK.errorhandler(404)
    def error_404(error):
        return back_404_data(), 404

    # 500
    @FLASK.errorhandler(500)
    def error_500(error):
        return back_500_data(), 500

    pass

# html，验证请求的必要参数
def flask_middleware_html(_request, route_data, back_data):
    method = _request.method
    url = _request.url
    # print_log("flask_request_html=", method, _request.headers, _request.url)
    #
    way = route_data["way"]
    methods = route_data["methods"]

    # 返回数据
    response = make_response(back_data)

    # 验证参数
    reg_method_state = check_req_methods(method, methods) # 拦截请求方法
    reg_url_state = check_req_url(url) # 拦截网址
    if reg_method_state and reg_url_state:
        reg_code = 200
    else:
        reg_code = 404

    #
    return flask_response_header(response, way, reg_code), reg_code

# 接口，验证请求的必要参数
def flask_middleware_api(_request, route_data, back_data):
    method = _request.method
    url = _request.url
    # print_log("flask_request_api=", method, _request.headers, _request.url)
    #
    way = route_data["way"]
    methods = route_data["methods"]

    # 返回数据
    response = make_response(jsonify(back_data))

    # 验证参数
    reg_method_state = check_req_methods(method, methods)  # 拦截请求方法
    reg_url_state = check_req_url(url)  # 拦截网址
    if reg_method_state and reg_url_state:
        reg_code = 200
    else:
        reg_code = 404

    #
    return flask_response_header(response, way, reg_code), reg_code

# 文件类型，验证请求的必要参数
def flask_middleware_file(_request, route_data, back_data):
    method = _request.method
    url = _request.url
    # print_log("flask_request_api=", method, _request.headers, _request.url)
    #
    way = route_data["way"]
    methods = route_data["methods"]

    # 返回数据
    response = make_response(jsonify(back_data))

    # 验证参数
    reg_method_state = check_req_methods(method, methods)  # 拦截请求方法
    reg_url_state = check_req_url(url)  # 拦截网址
    print("reg_state=", [reg_method_state, reg_url_state])
    if reg_method_state and reg_url_state:
        reg_code = 200
    else:
        reg_code = 404

    #
    return flask_response_header(response, way, reg_code), reg_code

# 检测请求方法是否在白名单
def check_req_methods(now_method, methods):
    if now_method in methods: # OK
        return True
    else: # "method Error"
        return False

# 检测网址是否在白名单
def check_req_url(full_url):
    white_hosts = CONFIG["flask"]["white_hosts"]
    for the_host in white_hosts:
        position = full_url.find(the_host)
        if 0 <= position <= len(the_host) and len(the_host)>=9: # OK
            return True
        else:
            continue
    return False

# 设置header
# way= html json file, filename含后缀, filetype=pdf png zip xlsx txt
def flask_response_header(response, way, reg_code=404, filename="", filetype=""):
    #
    response.status_code = reg_code
    response.headers["Header-Way"] = way
    response.headers["Author"] = CONFIG["app"]["author"]
    response.headers["App-Name"] = CONFIG["app"]["app_name"]
    #
    if way == "html" or way == "view"  or way == "tpl": # html
        response.headers["Content-Type"] = "text/html; charset=utf-8"
        response.headers["Cache-Control"] = "max-age=600"  # s
    elif way == "json" or way == "api": # api
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        response.headers["Cache-Control"] = "max-age=120"  # s
    else: # 文件，file
        response.headers["Content-Disposition"] = "attachment"
        response.headers["Cache-Control"] = "max-age=1200"  # s
        response.headers["filename"] = filename
        match filetype:
            case "pdf":
                response.headers["Content-Type"] = "application/pdf"
            case "txt":
                response.headers["Content-Type"] = "application/plain"
            case "zip":
                response.headers["Content-Type"] = "application/zip"
            case "7z":
                response.headers["Content-Type"] = "application/7z"
            case "png":
                response.headers["mimetype"] = filetype
            case "jpg":
                response.headers["mimetype"] = filetype
            case "jpeg":
                response.headers["mimetype"] = filetype
            case "gif":
                response.headers["mimetype"] = filetype
            case "xlsx":
                response.headers["mimetype"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            case _: # 其它情况
                response.headers["Content-Type"] = filetype
        pass
    #
    return response

# 启动Flask服务
def run_flask(window, pid):
    # 读取配置信息
    global CONFIG
    CONFIG = get_config("run_flask")
    #
    print_log("### Flask => ", "http://127.0.0.1:" + str(CONFIG["flask"]["port"])+"/api")
    #
    FLASK = Flask(__name__)
    # 必要路由
    must_routes(FLASK)
    # 注册自定义路由
    custom_routes_html(FLASK, flask_middleware_html)
    custom_routes_api(FLASK, flask_middleware_api, window)
    custom_routes_file(FLASK, flask_middleware_file)
    #
    FLASK.run(debug=CONFIG["flask"]["debug"], port=CONFIG["flask"]["port"])

    pass