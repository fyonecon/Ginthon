
# py_run_js对照表
# 页面url=on_load后执行
def list_py_run_js(window, config, key, data_dict):
    #
    state = 0
    msg = "-"
    js_content = ""

    # 默认
    if key == "test" or len(key) == 0:
        js_content = rf"""
            console.log("py_run_js-test", "{key}", "{data_dict}");
        """
        state = 1
        msg = "默认Key"
        pass
    # ===========================================================




    # ===========================================================
    # else
    else:
        js_content = rf"""
            console.log("py_run_js-else", "{key}", "{data_dict}");
        """
        state = 0
        msg = "不白名单的Key"
        pass
    #
    result = window.evaluate_js(js_content, callback=True)
    print("py_run_js.py：", [state, msg, result])
    return state, msg, result