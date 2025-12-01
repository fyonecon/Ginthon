import threading
import webbrowser
import webview

from internal.app.window.window_display import set_window_display
from internal.common.func import is_url

# py_run_js对照表
def list_js_call_py(WINDOW, config, key, data_dict):
    #
    state = 0
    msg = "（null）"

    print("list_js_call_py=", [key, data_dict])

    # 默认
    # data_dict={}
    if key == "test" or len(key) == 0:
        js_content = rf"""
            console.log("js_call_py-test", {key}, {data_dict});
        """
        state = 1
        msg = "默认Key"
        result = WINDOW.evaluate_js(js_content)
        return state, msg, result
    # ===========================================================


    # 用新窗口打开目标链接
    # data_dict={url="", "title"="new window"}
    elif key == "open_url_with_new_window":
        if data_dict.get("url") and data_dict.get("title"):
            url = data_dict["url"]
            title = data_dict["title"]
            #
            def new_window():
                webview.create_window(
                    url=url, title=title,
                    min_size=(520, 520),
                    width=520, height=520,
                    hidden=False,
                    frameless=False,
                    text_select=True,
                    transparent=False,
                    background_color="#555555",
                )
                webview.start()
                print("独立窗口已关闭：", [title, url])
                pass
            #
            if is_url(url):
                # 创建线程
                t1 = threading.Thread(target=new_window)
                # 启动线程
                t1.start()
                # 等待线程结束
                t1.join()
                state = 1
                msg = "YES"
            else:
                state = 0
                msg = "url格式不正确"
        else:
            state = 0
            msg = "data_dict错误"
        return state, msg, ""


    # 用默认浏览器打开目标链接
    # data_dict={url="", "target"="_blank"}
    elif key == "open_url_with_default_browser":
        if data_dict.get("url") and data_dict.get("target"):
            url = data_dict["url"]
            target = data_dict["target"]
            if is_url(url):
                if target == "_self":
                    webbrowser.open_new_tab(url)
                elif target == "_blank":
                    webbrowser.open_new(url)
                else:
                    webbrowser.open(url)
                state = 1
                msg = "YES"
            else:
                state = 0
                msg = "url格式不正确"
        else:
            state = 0
            msg = "data_dict错误"
        return state, msg, ""

    # 用原始窗口打开新链接
    # data_dict={url=""}
    elif key == "open_url_with_master_window":
        if data_dict.get("url"):
            url = data_dict["url"]
            if is_url(url):
                WINDOW.load_url(url)
                state = 1
                msg = "YES"
            else:
                state = 0
                msg = "url格式不正确"
        else:
            state = 0
            msg = "data_dict错误"
        return state, msg, ""

    # js监听当前窗口是隐藏还是展示
    # data_dict={display="showing hiding"}
    elif key == "window_display":
        if data_dict.get("display"):
            display = data_dict["display"]
            if display == "hiding":
                state = 1
                msg = set_window_display("hiding")
            elif display == "showing":
                state = 1
                msg = set_window_display("showing")
            else :
                state = 0
                msg = "url格式不正确"
        else:
            state = 0
            msg = "data_dict错误"
        return state, msg, ""

    # js监听当前窗口的主题
    # data_dict={theme="dark light"}
    elif key == "window_theme":
        if data_dict.get("theme"):
            display = data_dict["theme"]
            if display == "dark":
                state = 1
                msg = "dark"
            elif display == "light":
                state = 1
                msg = "light"
            else:
                state = 0
                msg = "url格式不正确"
        else:
            state = 0
            msg = "data_dict错误"
        return state, msg, ""

    # 隐藏窗口
    # data_dict={}
    elif key == "window_hide":
        WINDOW.hide()
        return state, msg, set_window_display("hiding")

    # 显示窗口
    # data_dict={}
    elif key == "window_show":
        WINDOW.show()
        return state, msg, set_window_display("showing")


    # ===========================================================
    # else
    # data_dict={}
    else:
        js_content = rf"""
            console.log("py_run_js-else");
        """
        state = 0
        msg = "不白名单的Key"
        result = WINDOW.evaluate_js(js_content)
        return state, msg, result
    #