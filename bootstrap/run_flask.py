from flask import Flask, jsonify
from app.flask.routes import custom_routes_api, custom_routes_file
from flask import make_response, request

#
CONFIG = {}

# 必要路由
def must_routes(FLASK):
    # index
    @FLASK.route("/") # 路由名
    def index(): # 触发函数（函数名尽量和路由名一致）
        route_data = {
            "way": "html",
            "methods": ["GET", "POST", "OPTIONS"],
            "status_code": 200
        }
        html_data = f'<html><body><p>{CONFIG["app_name"]} v{CONFIG["app_version"]}</p></body></html>'
        response_data = flask_request_html(request, route_data, html_data)
        return response_data

    # api
    @FLASK.route("/api")  # 路由名
    def api():  # 触发函数（函数名尽量和路由名一致）
        route_data = {
            "way": "json",
            "methods": ["GET", "POST", "OPTIONS"],
            "status_code": 200
        }
        api_data = {
            "state": 1,
            "msg": "OK",
            "content": {}
        }
        response_data = flask_request_api(request, route_data, api_data)
        return response_data

    # 404
    @FLASK.errorhandler(404)
    def error_404(error):
        html_data = """
             <html>
                <body>
                    <h3>404</h3>
                </body>
                </html>
            """
        return html_data, 404

    # 500
    @FLASK.errorhandler(500)
    def error_500(error):
        html = """
             <html>
                <body>
                    <h3>500</h3>
                </body>
                </html>
            """
        return html, 500

    pass

# html，验证请求的必要参数
def flask_request_html(_request, route_data, back_data):
    method = _request.method
    #
    way = route_data["way"]
    methods = route_data["methods"]
    status_code = route_data["status_code"]
    # 返回数据
    response = make_response(back_data)
    # 自定义请求头
    response.headers["author"] = CONFIG["author"]
    response.headers["app_name"] = CONFIG["app_name"]
    # 拦截请求方法
    if method in methods:  # OK
        reg_code = status_code
    else:  # "method Error"
        reg_code = 404

    # 设置接口返回请求头
    flask_response(response, way, reg_code)
    return response

# 接口，验证请求的必要参数
def flask_request_api(_request, route_data, back_data):
    method = _request.method
    #
    way = route_data["way"]
    methods = route_data["methods"]
    status_code = route_data["status_code"]
    # 返回数据
    response = make_response(jsonify(back_data))
    # 自定义请求头
    response.headers["author"] = CONFIG["author"]
    response.headers["app_name"] = CONFIG["app_name"]
    # 拦截请求方法
    if method in methods: # OK
        reg_code = status_code
    else: # "method Error"
        reg_code = 404

    # 设置接口返回请求头
    flask_response(response, way, reg_code)
    return response

# 文件类型，验证请求的必要参数
def flask_request_file(_request, route_data, back_data):
    #。。。
    return

# 设置header
# way= html json file, filename含后缀, filetype=pdf png zip xlsx txt
def flask_response(response, way, status_code=200, filename="-", filetype=""):
    #
    response.status_code = status_code
    response.headers["author"] = CONFIG["author"]
    response.headers["app_name"] = CONFIG["app_name"]
    #
    if way == "html": # html
        response.headers["Content-Type"] = "text/html; charset=utf-8"
        response.headers["Cache-Control"] = "max-age=600"  # s
    elif way == "json": # api
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        response.headers["Cache-Control"] = "max-age=120"  # s
    else: # 文件
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

    pass

# 启动Flask服务
def run_flask(config):
    # 读取配置信息
    global CONFIG
    CONFIG = config
    #
    print("✅ Flask => ", "http://127.0.0.1:" + str(CONFIG["flask"]["port"])+"/api")
    #
    FLASK = Flask(__name__)
    # 必要路由
    must_routes(FLASK)
    # 注册自定义路由
    custom_routes_api(FLASK, flask_request_api)
    custom_routes_file(FLASK, flask_request_file)
    #
    FLASK.run(debug=CONFIG["flask"]["debug"], port=CONFIG["flask"]["port"])

    pass