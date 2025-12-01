import webbrowser
import webview
import threading

from internal.common.func import is_url

# 改变url
def load_new_url(window, new_url):
    window.load_url(new_url)
    pass

#
def set_title(window, new_title="Null Title"):
    window.set_title(new_title)
    pass

#
def destroy(window):
    window.destroy()
    pass

#
def hide(window):
    window.hide()
    pass

#
def show(window):
    window.show()
    pass

# 新窗口打开一个链接
def open_new_window(url, title):
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
        return True
    else:
        return False

# 打开默认浏览器
# _self新标签中打开，_blank新窗口中打开
def open_default_browser(url, target="_self"):
    if is_url(url):
        if target == "_self":
            webbrowser.open_new_tab(url)
        elif target == "_blank":
            webbrowser.open_new(url)
        else:
            webbrowser.open(url)
        return True
    else:
        return False

# py执行js
def py_run_js(window, js_txt='console.log("py_run_js");'):
    js_content = rf"""
        {js_txt}
        """
    result = window.evaluate_js(js_content)
    print("run_js：", result)
    pass