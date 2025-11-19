
# 改变url
def load_url(window, new_url):
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

# py执行js
def py_run_js(window, js_txt='console.log("py_run_js");'):
    js_content = rf"""
        {js_txt}
        """
    result = window.evaluate_js(js_content)
    print("run_js：", result)
    pass