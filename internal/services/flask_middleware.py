# -*- coding: utf-8 -*-

from flask import make_response, request, jsonify

from internal.common.func import func
from internal.config import get_config

#
CONFIG = get_config("", "")

# api接口，验证请求的必要参数，只能是json
def flask_middleware_api(_request, _back_data):
    url = _request.url
    # 响应
    response = make_response(jsonify(_back_data))

    # 验证参数
    reg_url_state = check_req_url(url)  # 拦截网址
    if  reg_url_state:
        reg_code = 200
    else:
        reg_code = 404

    # 返回标准headers
    return flask_response_header(response, "json", reg_code, ""), reg_code


# html，验证请求的必要参数，只能是html
def flask_middleware_html(_request, _back_data, _filename):
    url = _request.url
    # 响应
    response = make_response(_back_data)

    # 验证参数
    reg_url_state = check_req_url(url) # 拦截网址
    if reg_url_state:
        reg_code = 200
    else:
        reg_code = 404

    # 返回标准headers
    return flask_response_header(response, "html", reg_code, _filename), reg_code

# 文件类型，验证请求的必要参数，可以是txt、js、image、zip等多种格式的file
def flask_middleware_file(_request, _back_data, _filename):
    url = _request.url
    # 响应
    response = make_response(_back_data)

    # 验证参数
    reg_url_state = check_req_url(url)  # 拦截网址
    if reg_url_state:
        reg_code = 200
    else:
        reg_code = 404

    # 返回标准headers
    return flask_response_header(response, "file", reg_code, _filename), reg_code

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
def flask_response_header(response, way, reg_code=200, filename=""):
    #
    response.status_code = reg_code
    response.headers["Way"] = way
    response.headers["Author"] = CONFIG["app"]["author"]
    #
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
    # response.headers['Access-Control-Allow-Credentials'] = 'true' # true不能与*一起使用
    response.headers['Access-Control-Max-Age'] = '30'
    #
    if way == "html" or way == "view": # html
        response.headers["Content-Disposition"] = "inline"
        response.headers["Content-Type"] = func.get_file_ext_mimetype(".html")
        response.headers["Cache-Control"] = "max-age=60"  # s
        response.headers["filename"] = filename
    elif way == "json" or way == "api": # api
        response.headers["Content-Disposition"] = "inline"
        response.headers["Content-Type"] = func.get_file_ext_mimetype(".json")
        response.headers["Cache-Control"] = "max-age=60"  # s
    else: # 文件，file
        response.headers["Content-Disposition"] = "attachment"
        response.headers["Cache-Control"] = "max-age=120"  # s
        response.headers["filename"] = filename
        response.headers["Content-Type"] = func.get_file_ext_mimetype(func.get_file_ext(filename))
    #
    return response
