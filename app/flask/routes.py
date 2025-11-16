from flask import Flask, jsonify, send_file, request

# 自定义路由
def custom_routes_api(FLASK, flask_request_api):
    #
    @FLASK.route("/api/<txt>")  # 路由名
    def text(txt):  # 触发函数（函数名尽量和路由名一致）
        route_data = {
            "way": "json",
            "methods": ["GET", "POST", "OPTIONS"],
            "status_code": 200
        }
        api_data = {
            "state": 1,
            "msg": "OK",
            "content": {
                "txt": txt,
            }
        }
        response_data = flask_request_api(request, route_data, api_data)
        return response_data

    pass

# 自定义路由
def custom_routes_file(FLASK, flask_request_file):
    #
    @FLASK.route("/file/<filename>")  # 路由名
    def file(filename):  # 触发函数（函数名尽量和路由名一致）
        filetype = ""
        # flask_response("file", status_code=200, filename=filename, filetype=filetype)
        file_path = 'xx/xx.pdf'
        return send_file(file_path, as_attachment=True)

    pass