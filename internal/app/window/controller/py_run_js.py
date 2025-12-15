# -*- coding: utf-8 -*-

from internal.common.app_auth import make_rand_id, make_rand_token
from internal.common.func import print_log, md5
from internal.config import get_config


# py_run_js对照表
# 页面url=on_load后执行
def list_py_run_js(window, key, data_dict):
    #
    CONFIG = get_config("", "")
    #
    state = 0
    msg = ""
    content = {}
    js_content = ""

    #
    if key == "test" or len(key) == 0: # 默认
        js_content = rf'''
            console.log("[视窗PY-Log]", "py_run_js-test", [window.location.href, "{key}", "{data_dict}"]);
        '''
        #
        state = 1
        msg = "默认Key"
        pass
    # elif key == "window_token": # 默认
    #     window_token = make_rand_id(CONFIG)  # 视窗软件启动时会生成一个新的
    #     js_content = f'''
    #         localStorage.setItem("window_token", "{window_token}");
    #     '''
    #     #
    #     state = 1
    #     msg = "写入window_token"
    #     pass
    # 其它
    #
    # else
    else: # 默认
        js_content = rf"""
            console.log("[视窗PY-Log]", "py_run_js-else", [window.location.href, "{key}", "{data_dict}"]);
        """
        state = 0
        msg = "不白名单的Key"
        pass

    # ===
    result = window.evaluate_js(js_content, callback=True)
    content["result"] = result
    print_log("py_run_js.py：", key, [state, msg, result])
    return {
        "state": state,
        "msg": msg,
        "content": content,
    }