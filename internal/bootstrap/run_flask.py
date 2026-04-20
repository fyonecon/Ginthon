# -*- coding: utf-8 -*-

from flask import Flask, jsonify, send_file
from flask import request

from internal.routes.flask_http_api import flask_http_api
from internal.routes.flask_http_file import flask_http_file
from internal.routes.flask_http_html import flask_http_html
from internal.routes.route_must import route_must
from internal.routes.route_window import route_window
from internal.common.func import func
from internal.common.kits.ssl_127 import ssl_127
from internal.common.request_data import request_data
from internal.routes.flask_ws import flask_ws

#
CONFIG = {}


# 启动Flask服务
def run_flask(window, webview_pid, config):
    # 读取配置信息
    global CONFIG
    CONFIG = config
    #
    ssl_state = CONFIG["flask"]["ssl"]
    if ssl_state:
        s = "s"
        pass
    else:
        s = ""
        pass
    func.print_log("### Flask => ", "http"+s+"://127.0.0.1" + ":" + str(CONFIG["flask"]["port"])+"/api")
    #
    FLASK = Flask(__name__)

    # 装饰器
    @FLASK.before_request
    def before_request():
        """全局处理 OPTIONS 请求"""
        if request.method == 'OPTIONS':
            response = jsonify()
            response.headers.add("Author", CONFIG["app"]["author"])
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Requested-With')
            response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            return response
        else:
            return None

    # flask必要路由
    route_must(window, FLASK)
    # window必要路由
    route_window(window, FLASK)

    # 注册自定义路由
    flask_http_html(window, FLASK)
    flask_http_api(window, FLASK)
    flask_http_file(window, FLASK)
    flask_ws(window, FLASK)

    # 启动Flask
    no_ssl_host = "0.0.0.0" # 0.0.0.0
    ssl_host = "127.0.0.1" # 0.0.0.0、127.0.0.1
    if ssl_state:
        FLASK.run(debug=CONFIG["flask"]["debug"], ssl_context=ssl_127.read_ssl_context(host=ssl_host), host=ssl_host, port=CONFIG["flask"]["port"])
        pass
    else:
        FLASK.run(debug=CONFIG["flask"]["debug"], host=no_ssl_host, port=CONFIG["flask"]["port"])
        pass

    # 检测端口在check_sys中，此处不再检测。

    pass