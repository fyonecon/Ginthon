# -*- coding: utf-8 -*-

from internal.common.kits.txt_data import txt_data
from internal.config import get_config

#
CONFIG = get_config("", "")

# 原理：使用js监测窗口的display，然后js_call_py实现state值持久化保存在本地

class display_state:

    # 记录当前窗口隐藏状态
    # display=hiding showing
    @staticmethod
    def set(display="hiding"):
        global CONFIG
        running_filename = "display_state.cache"
        txt_data.remove(running_filename)
        txt_data.write(running_filename, display)
        return display

    # 读取当前窗口隐藏状态
    @staticmethod
    def get():
        global CONFIG
        running_filename = "display_state.cache"
        return txt_data.read(running_filename)

    #
    pass

