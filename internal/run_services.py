import threading

from time import sleep
from common.config import get_config
from common.func import get_date, print_log
from common.time_interval import do_time_interval
from common.txt_data import txt_read, txt_remove
from internal.watch_processes import watch_processes

#
CONFIG = {}
process_pids_txt = None

# 周期服务
def start_time_interval():
    tag = "run_service_1"
    print_log("🚩周期服务：", "tag="+tag)
    #
    global process_pids_txt
    def do_timer1():
        print_log("do_timer=1=", get_date("%Y-%m-%d %H:%M:%S"))
        # pids值只获取一次，除非为空
        global process_pids_txt
        txt_filename = "running/process_pids.cache"
        #
        pid1 = 0
        pid2 = 0
        pid3 = 0
        #
        if process_pids_txt is None:
            try:
                txt_content = txt_read(txt_filename)
                if len(txt_content) > 2: # 有完整值
                    txt_remove(txt_filename) # 用完后直接删除
                    #
                    process_pids_txt = txt_content
                    process_pids = process_pids_txt.split("#@")
                    pid1 = int(process_pids[0])
                    pid2 = int(process_pids[1])
                    pid3 = int(process_pids[2])
                else: # 无值则直接删除文件
                    print("❌ 文件中的值不完整：", txt_filename)
                    pass
            except:
                print("❌ 文件可能不存在：", txt_filename)
                pass
        else:
            process_pids = process_pids_txt.split("#@")
            pid1 = int(process_pids[0])
            pid2 = int(process_pids[1])
            pid3 = int(process_pids[2])
            pass
        # 检测进程是否完整
        print_log("process_pids_txt=", process_pids_txt)
        watch_processes(pid1, pid2, pid3)
        pass

    do_time_interval(5, do_timer1, tag, CONFIG)
    pass

# 启动服务
def run_services():
    print("✅ 后台服务 => ", get_date("%Y-%m-%d %H:%M:%S"))

    # 读取配置信息
    global CONFIG
    CONFIG = get_config("run_services")
    #
    sleep(2)

    # 创建线程
    t1 = threading.Thread(target=start_time_interval)

    # 启动线程
    t1.start()

    # 等待线程结束
    t1.join()

    print("❌服务运行结束，线程中断。")
    pass