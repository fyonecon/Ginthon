# -*- coding: utf-8 -*-
from flask import send_file, request

from internal.app.flask.app_token import check_app_token
from internal.services.flask_middleware import flask_middleware_file
from internal.common.func import func
from internal.common.request_data import request_data


# 自定义路由，文件专用
def flask_http_file(_WINDOW, FLASK):

    # 适配音乐播放及访问本地文件
    # http://127.0.0.1:9750/dir/play_audio/xxx
    @FLASK.route("/dir/play_audio/<path:filepath>", methods=["GET", "POST", "OPTIONS"], endpoint="play_audio")
    def play_audio(filepath):
        route_data = {
            "way": "file",
            "methods": ["GET", "POST", "OPTIONS"],
        }
        #
        file_token = request_data.input(request, "file_token")
        # 还原真实文件
        filepath = func.url_decode(filepath)
        filepath = func.converted_path(filepath)
        if func.get_platform() == "mac":  # 解决目录无前缀
            filepath = "/" + filepath
            filepath = filepath.replace("//", "/")
            pass
        #
        file_token_state = func.md5("file=" + func.url_encode(filepath)) == file_token
        app_token_state = check_app_token(request, "app")
        #
        if file_token_state and app_token_state:
            filename = func.get_file_name(filepath)
            file_ext = func.get_file_ext(filename)
            if len(file_ext) >= 1:  # 有文件
                mimetype = func.get_file_ext_mimetype(file_ext)
                file_path = filepath  # 限定根目录
                #
                if func.has_file(file_path):
                    response_data, reg_code = flask_middleware_file(request, route_data, "", filename)
                    if reg_code == 200:
                        # 使用返回文件的方式返回html模板或文件
                        return send_file(file_path, as_attachment=False, mimetype=mimetype, max_age=12 * 60, download_name=filename), reg_code
                    else:
                        return func.back_404_data_file("非法操作：file"), reg_code
                else:
                    return func.back_404_data_file("无对应文件：" + filepath + "🌛" + filename), 404
            else:
                return func.back_404_data_file("无对应文件：" + filepath + "🌞" + filename), 404
        else:
            return func.back_404_data_file("非法Auth，token"), 404

    # file

    # file
    pass
