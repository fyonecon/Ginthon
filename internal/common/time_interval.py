import schedule
import time
from internal.common.func import get_time_ms, get_date

# 周期任务，最少5s，最大365天
def do_time_interval(timeout_s, call_func, tag="", config=None):
    # 默认值，s
    min_timer = 5
    max_timer = 365*24*60*60
    if timeout_s < min_timer:
        timeout_s = min_timer
    elif timeout_s > max_timer:
        timeout_s = max_timer
    else:
        pass
    #
    # print("周期服务已开启，tag="+tag, str(timeout_s)+"s", get_date("%Y-%m-%d %H:%M:%S"))
    schedule.every(timeout_s).seconds.do(call_func)
    while True:
        schedule.run_pending()
        time.sleep(1)
    pass

# 调用
# 开启周期任务
# def do_timer1():
#     print("do_timer=1=", get_date("%Y-%m-%d %H:%M:%S"))
#     pass
# do_time_interval(10, do_timer1, "test")