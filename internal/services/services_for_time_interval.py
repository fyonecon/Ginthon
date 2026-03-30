# -*- coding: utf-8 -*-

from time import sleep

from internal.common.kits.time_interval import time_interval

#
CONFIG = {}


# 周期服务，默认10s
def services_for_time_interval(_WINDOW, _webview_pid, _config):
    #
    global CONFIG
    CONFIG = _config

    sleep(1)
    tag = "run_service_1"
    # print_log("🚩周期服务：", "tag="+tag)
    #
    def do_timer1():
        # print_log("do_timer=1=", get_date("%Y-%m-%d %H:%M:%S"))
        #
        pass
    time_interval.do_time_interval(6, do_timer1, tag, CONFIG)
    pass
