# -*- coding: utf-8 -*-

import os

from internal.app.window.controller.display_state import get_display_state, set_display_state
from internal.common.kits.watch_pid import kill_process_by_pid


#
def tray_events(_WINDOW, do):
    window_show_hide_state = ""  # 视窗当前是否显示，需要从本地视窗获取状态（待定） “” show hide
    #
    if do == "app@show_or_hide":
        state = 1
        msg = "show_or_hide"
        display = get_display_state()
        print("tray_events", do, display)
        if display == "showing":
            set_display_state("hiding")
            _WINDOW.hide()
        else:
            set_display_state("showing")
            _WINDOW.show()
        pass
    elif do == "app@about":
        state = 1
        msg = "about"
        #
        pass
    elif do == "app@exit":  # exit
        state = 1
        msg = "exit"
        # 杀掉主程序（全部程序）
        main_pid = os.getpid()
        kill_process_by_pid(main_pid)
        #
        pass
    else:  # 未知状态
        state = 0
        msg = "未知状态：" + do
        pass
    return state, msg
    pass