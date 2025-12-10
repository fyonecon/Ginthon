from flask import make_response, request, jsonify

from internal.common.func import get_file_ext, get_file_ext_mimetype
from internal.config import get_config

#
CONFIG = get_config("", "")

# html，验证请求的必要参数
def flask_middleware_html(_request, route_data, back_data, filename):
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
    return flask_response_header(response, way, reg_code, filename), reg_code

# 接口，验证请求的必要参数
def flask_middleware_api(_request, route_data, back_data, filename=""):
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
    return flask_response_header(response, way, reg_code, ""), reg_code

# 文件类型，验证请求的必要参数
def flask_middleware_file(_request, route_data, back_data, filename):
    method = _request.method
    url = _request.url
    # print_log("flask_request_api=", method, _request.headers, _request.url)
    #
    way = route_data["way"]
    methods = route_data["methods"]

    # 返回数据
    response = make_response(back_data)

    # 验证参数
    reg_method_state = check_req_methods(method, methods)  # 拦截请求方法
    reg_url_state = check_req_url(url)  # 拦截网址
    # print("reg_state=", [reg_method_state, reg_url_state])
    if reg_method_state and reg_url_state:
        reg_code = 200
    else:
        reg_code = 404

    #
    return flask_response_header(response, way, reg_code, filename), reg_code

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
# way= html json file, filename含后缀,
def flask_response_header(response, way, reg_code=404, filename=""):
    #
    response.status_code = reg_code
    response.headers["Header-Way"] = way
    response.headers["Author"] = CONFIG["app"]["author"]
    response.headers["App-Name"] = CONFIG["app"]["app_name"]
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    #
    if way == "html" or way == "view": # html
        response.headers["Content-Disposition"] = "inline"
        response.headers["Content-Type"] = get_file_ext_mimetype(".html")
        response.headers["Cache-Control"] = "max-age=120"  # s
        response.headers["filename"] = filename
    elif way == "json" or way == "api": # api
        response.headers["Content-Disposition"] = "inline"
        response.headers["Content-Type"] = get_file_ext_mimetype(".json")
        response.headers["Cache-Control"] = "max-age=120"  # s
    else: # 文件，file
        response.headers["Content-Disposition"] = "attachment"
        response.headers["Cache-Control"] = "max-age=120"  # s
        response.headers["filename"] = filename
        file_ext = get_file_ext(filename)
        response.headers["Content-Type"] = get_file_ext_mimetype(file_ext)
    #
    return response
