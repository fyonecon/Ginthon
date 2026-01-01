# -*- coding: utf-8 -*-

import sys
from time import sleep

from internal.app.window.controller.py_run_js import list_py_run_js
from internal.common.app_auth import make_rand_id, make_rand_token
from internal.common.func import func
from internal.config import get_config

def on_initialized():
    func.print_log('pywebview window is on_initialized')
    pass

def on_closing(window):
    func.print_log('pywebview window is closing')
    pass

def on_closed(window):
    func.print_log('pywebview window is closed')
    sys.exit(1)
    pass

def on_before_show(window):
    func.print_log('pywebview window is on_before_show')
    pass

def on_shown(window):
    func.print_log('pywebview window shown')
    pass

# def on_hidden(window):
#     func.print_log('pywebview window hidden')
#     pass

def on_minimized(window):
    func.print_log('pywebview window minimized')
    pass

def on_restored(window):
    func.print_log('pywebview window restored')
    pass

def on_maximized(window):
    func.print_log('pywebview window maximized')
    pass

def on_before_load(window):
    func.print_log('DOM is on_before_load')
    pass

def on_loaded(window):
    func.print_log('DOM is ready')
    #
    # CONFIG = get_config("", "")

    # test
    list_py_run_js(window, "test", {"key1": "test 111"})

    #
    pass

def on_resized(window, width, height):
    # func.print_log('pywebview window is resized. new dimensions are {width} x {height}'.format(width=width, height=height))
    pass

def on_moved(window, x, y):
    # func.print_log('pywebview window is moved. new coordinates are x: {x}, y: {y}'.format(x=x, y=y))
    pass