# -*- coding: utf-8 -*-

from internal.common.func import func
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
    func.print_log("py_run_js.py：", key, [state, msg, result])
    return {
        "state": state,
        "msg": msg,
        "content": content,
    }