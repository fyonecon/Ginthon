# -*- coding: utf-8 -*-

import os

from flask import send_file, request

from internal.app.app_flask.app_token import check_app_token
from internal.app.app_flask.http_controller.play_audio import get_play_audio_list
from internal.app.app_flask.http_controller.spider_ithome import read_spider_it_home
from internal.services.flask_middleware import flask_middleware_api
from internal.common.func import func


# 自定义路由，接口专用
def flask_http_api(_WINDOW, FLASK):

    # http://127.0.0.1:9750/api/spider/ithome
    @FLASK.route("/api/spider/ithome", methods=["GET", "POST", "OPTIONS"])  # 路由名
    def api_spider_ithome():  # 触发函数（函数名尽量和路由名一致）
        # app_token
        app_token_state = check_app_token(request, "app")
        if app_token_state:
            # 返回的数据
            back_data = read_spider_it_home(request)

            # 用中间件验证参数
            response_data, reg_code = flask_middleware_api(_request=request, _back_data=back_data)
            #
            if reg_code == 200:
                return response_data, reg_code
            else:
                return func.back_404_data_api("非法操作:api"), reg_code
        else:
            return func.back_404_data_api("非法Auth:api"), 404


    # http://127.0.0.1:9750/api/get_play_audio_list
    @FLASK.route("/api/get_play_audio_list", methods=["GET", "POST", "OPTIONS"])  # 路由名
    def api_play_audio():  # 触发函数（函数名尽量和路由名一致）
        # app_token
        app_token_state = check_app_token(request, "app")
        if app_token_state:
            # 返回的数据
            back_data = get_play_audio_list(request)

            # 用中间件验证参数
            response_data, reg_code = flask_middleware_api(_request=request, _back_data=back_data)
            if reg_code == 200:
                return response_data, reg_code
            else:
                return func.back_404_data_api("非法操作:api"), reg_code
        else:
            return func.back_404_data_api("非法Auth:api"), 404

    # api
    pass
