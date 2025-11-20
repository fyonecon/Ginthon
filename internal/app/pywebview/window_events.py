import sys


# 获取当前window对象
def current_window(window):
    print("current_window")
    pass

def on_closed():
    print('pywebview window is closed')
    sys.exit(1)
    pass

def on_before_load():
    print('pywebview window is on_before_load')
    pass

def on_before_show():
    print('pywebview window is on_before_show')
    pass

def on_initialized():
    print('pywebview window is on_initialized')
    pass

def on_closing():
    print('pywebview window is closing')
    pass

def on_shown():
    print('pywebview window shown')
    pass

def on_minimized():
    print('pywebview window minimized')
    pass

def on_restored():
    print('pywebview window restored')
    pass

def on_maximized():
    print('pywebview window maximized')
    pass

def on_loaded():
    print('DOM is ready')
    pass

def on_resized(width, height):
    print('pywebview window is resized. new dimensions are {width} x {height}'.format(width=width, height=height))
    pass

def on_moved(x, y):
    # print('pywebview window is moved. new coordinates are x: {x}, y: {y}'.format(x=x, y=y))
    pass