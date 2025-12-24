# -*- coding: utf-8 -*-

from flask import send_file, request
from internal.bootstrap.flask_middleware import flask_middleware_file
from internal.common.func import back_404_data_file, get_file_ext, get_file_ext_mimetype, has_file
from internal.common.kits.main_dirpath import mian_virtual_dirpath


# 自定义路由，文件专用
def flask_route_file(_WINDOW, FLASK):

    # 静态文件系统 http://127.0.0.1:9750/file/test.txt
    @FLASK.route("/play_audio/<path:filename>", methods=["GET", "POST", "OPTIONS"])
    def play_audio(filename):
        route_data = {
            "way": "file",
            "methods": ["GET", "POST", "OPTIONS"],
        }
        # 还原真实文件
        file_ext = get_file_ext(filename)
        if len(file_ext) >= 1:  # 有文件
            file_ext = get_file_ext(filename)
            mimetype = get_file_ext_mimetype(file_ext)
            file_path = mian_virtual_dirpath("frontend") + "/file" + "/" + filename  # 限定根目录
            #
            if has_file(file_path):
                response_data, reg_code = flask_middleware_file(request, route_data, "", filename)
                if reg_code == 200:
                    # 使用返回文件的方式返回html模板或文件
                    return send_file(file_path, as_attachment=False, mimetype=mimetype, max_age=12 * 60,
                                     download_name=filename), reg_code
                else:
                    return back_404_data_file("非法操作：file"), reg_code
            else:
                return back_404_data_file("无对应文件：" + filename), 404
        else:
            return back_404_data_file("无对应文件：" + filename), 404

    # file


    # file
    pass
