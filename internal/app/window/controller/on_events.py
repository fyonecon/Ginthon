import sys
from time import sleep

from internal.app.window.controller.py_run_js import list_py_run_js
from internal.bootstrap.app_auth import make_rand_id
from internal.common.func import print_log
from internal.config import get_config


def on_closed(window):
    print_log('pywebview window is closed')
    sys.exit(1)
    pass

def on_before_load(window):
    print_log('pywebview window is on_before_load')
    pass

def on_before_show(window):
    print_log('pywebview window is on_before_show')
    pass

def on_initialized():
    print_log('pywebview window is on_initialized')
    pass

def on_closing(window):
    print_log('pywebview window is closing')
    pass

def on_shown(window):
    print_log('pywebview window shown')
    pass

# def on_hidden(window):
#     print_log('pywebview window hidden')
#     pass

def on_minimized(window):
    print_log('pywebview window minimized')
    pass

def on_restored(window):
    print_log('pywebview window restored')
    pass

def on_maximized(window):
    print_log('pywebview window maximized')
    pass

def on_loaded(window):
    print_log('DOM is ready')
    #
    CONFIG = get_config("")
    #
    current_uid = window.uid
    current_url = window.get_current_url()
    if current_url is None:
        current_url = "（current_url使用了html直接渲染）"
        pass
    print_log("当前窗口DOM=", [current_uid, current_url])
    window_token = make_rand_id(CONFIG) # 视窗软件启动时会生成一个新的
    # 1
    script = f'''
        localStorage.setItem("window_token", "{window_token}");
        console.log("[视窗PY-Log]", "PY写入视窗的信息：", ["{current_uid}", window.location.href, "{window_token}"]);
    '''
    window.evaluate_js(script, callback=None)
    # 2
    list_py_run_js(window, CONFIG, "test", {"key1": "111"})
    #
    pass

def on_resized(window, width, height):
    print_log('pywebview window is resized. new dimensions are {width} x {height}'.format(width=width, height=height))
    pass

def on_moved(window, x, y):
    print_log('pywebview window is moved. new coordinates are x: {x}, y: {y}'.format(x=x, y=y))
    pass