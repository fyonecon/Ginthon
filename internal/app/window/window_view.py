# -*- coding: utf-8 -*-

from internal.common.app_auth import make_rand_token, make_rand_id
from internal.common.func import get_time_s, get_date, md5
from internal.common.kits.main_dirpath import mian_virtual_dirpath
import os

from internal.config import get_config

#
def view_js_must_data():
    #
    CONFIG = get_config("", "")
    #
    window_token = make_rand_id(CONFIG)  # 视窗软件启动时会生成一个新的
    js_token = f'''
        localStorage.setItem("window_token", "{window_token}"); 
    '''
    #
    view_host = CONFIG["pywebview"]["view_host"]
    # view_file_html = CONFIG["pywebview"]["view_file_html"]
    # view_url = view_host + ":" + str(CONFIG["flask"]["port"]) + "/" + view_file_html
    view_url = view_host + ":" + str(CONFIG["flask"]["port"]) + "/"
    app_class = CONFIG["app"]["app_class"]
    salt_str = "js_call_py_auth-2025"
    timeout_s = 2 * 365 * 24 * 3600
    app_token = make_rand_token(app_class, md5(salt_str + "nbPlus"), timeout_s, CONFIG)  # page刷新时会生成一个新的
    js_call_py_auth = make_rand_token(app_class, salt_str, timeout_s, CONFIG)  # 视窗软件启动时会生成一个新的
    js_call_py_api = view_host + ":" + str(CONFIG["flask"]["port"]) + "/api/js_call_py"
    js_must_data = f'''
       const app_token = "{app_token}";
       const view_url = "{view_url}";
       const js_call_py_api = "{js_call_py_api}"; 
       const js_call_py_auth = "{js_call_py_auth}"; 
   '''
    return js_token + js_must_data


# 视图view（针对单页应用最佳）
def view_index(_WINDOW, filename):
    #
    def read_html(the_file):
        content = ""
        if os.path.exists(the_file):  # 存在文件或文件夹
            if os.path.isfile(the_file):  # 是文件
                with open(the_file, "r", encoding="utf-8") as file:
                    content = file.read()
                    pass
        return content
    #
    CONFIG = get_config("", "")
    #
    view_host = CONFIG["pywebview"]["view_host"]
    view_file_html = CONFIG["pywebview"]["view_file_html"]
    file_path = mian_virtual_dirpath("frontend") + "/"+view_file_html+"/"+filename
    #
    js_must_data_url = view_host+":"+str(CONFIG["flask"]["port"])+"/"+ "js_must_data.js" + "?cache=" + str(get_time_s()) + "&app_version=" + CONFIG["app"]["app_version"]
    #
    html = read_html(file_path)
    # loaded后执行
    js_loaded = f'''
            <script src="{js_must_data_url}"></script>
        '''
    # 为空时的默认DOM
    if len(html)==0:
        html = '''
        <html lang="zh">
        <head>
            <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0, user-scalable=0" />
            <link rel="apple-touch-icon" href="/icon.png">
            <link rel="shortcut icon" href="/favicon.ico" type="image/x-icon" />
            <title>Default Window</title>
            <style>
                .hide{
                    display: none !important;
                }
                .click{
                    cursor: pointer;
                }
                .click:active{
                    opacity: 0.6;
                }
                .select-none{
                    -moz-user-select: none;-webkit-user-select: none;-ms-user-select: none;user-select: none;
                }
                .break{
                    overflow: hidden;
                    word-wrap: break-word;
                    overflow-wrap: break-word;
                }
            </style>
        </head>
        <body style="background-color: transparent;">
            <br/>
            <h2 style="text-align: center;" class="select-none pywebview-drag-region" >当前使用了空模板。</h2>
            <div style="text-align: center;">
                <p id="info" class="break"></p>
                <p class="select-none"><img src="http://127.0.0.1:9750/file/test.png" width="192" alt=""/></p>
            </div>
            <script>
            function show_info(_view_html) {
                let info = [
                    window.location.host, 
                    !!window.localStorage, 
                    !!window.indexedDB, 
                    navigator.webdriver, 
                    navigator.languages, 
                    window.matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light", "✅", 
                    window.navigator.userAgent,
                    view_url,
                    view_html,
                ]; 
                console.log(info);
                document.getElementById("info").innerHTML = view_filename+" 文件不存在。"; 
            }
            show_info(view_html);
            </script>
        </body>
        </html>
        '''
        pass

    return html+js_loaded