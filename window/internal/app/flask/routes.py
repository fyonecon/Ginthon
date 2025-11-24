from flask import send_file, request

from internal.common.view_auth import check_view_rand_id


# 自定义路由，视图专用
def custom_routes_html(FLASK, flask_request_html):
    #
    @FLASK.get("/html/view/<view_rand_id>")
    def html(view_rand_id):
        route_data = {
            "way": "html",
            "methods": ["GET"],
            "status_code": 200
        }
        rand_id_state = check_view_rand_id(view_rand_id)
        if rand_id_state: # 正确ID
            html_data = '''
            html
            '''
        else: # 非法ID
            html_data = '''
            Error URL.
            '''
        response_data = flask_request_html(request, route_data, html_data)
        return response_data

    pass

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