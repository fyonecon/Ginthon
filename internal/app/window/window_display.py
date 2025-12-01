from internal.common.kits.txt_data import txt_remove, txt_write, txt_read
from internal.config import get_config

#
CONFIG = get_config("")

# 原理：使用js监测窗口的display，然后js_call_py实现state值持久化保存在本地

# 记录当前窗口隐藏状态
# display=hiding showing
def set_window_display(display="hiding"):
    global CONFIG
    running_id_filename = CONFIG["app"]["app_class"]+"display_state.cache"
    txt_remove(running_id_filename)
    txt_write(running_id_filename, display)
    return display

# 读取当前窗口隐藏状态
def get_window_display():
    global CONFIG

    running_id_filename = CONFIG["app"]["app_class"]+"display_state.cache"
    return txt_read(running_id_filename)