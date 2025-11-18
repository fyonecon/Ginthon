import psutil
import time
import threading

from time import sleep

from common.func import print_log
from common.time_interval import do_time_interval

# 杀掉特定pid进程
def kill_pid_process(pid, timeout=6):
    try:
        process = psutil.Process(pid)

        print_log(f"准备终止进程: {process.name()} (PID: {pid})")
        print_log(f"进程状态: {process.status()}", process.is_running())
        print_log(f"启动时间: {time.ctime(process.create_time())}")

        # 优雅终止
        process.terminate()

        # 等待进程结束
        try:
            process.wait(timeout=timeout)
            print_log(f"进程 {pid} 已优雅终止")
            return True
        except psutil.TimeoutExpired:
            # 强制终止
            print_log(f"进程 {pid} 未响应，强制终止...")
            process.kill()
            process.wait()
            print_log(f"进程 {pid} 已强制终止")
            return True

    except psutil.NoSuchProcess:
        print(f"❌ 进程 {pid} 不存在")
        return False
    except psutil.AccessDenied:
        print(f"❌ 没有权限终止进程 {pid}")
        return False
    except Exception as e:
        print(f"❌ 终止进程 {pid} 时出错: {e}")
        return False

#
def watch_pid():
    # print("🚩检测进程：watch_pid=", process1_pid, process2_pid, process3_pid)
    sleep(2)
    #
    tag = "watch_processes"
    def do_pid_killer():
        process3 = psutil.Process(process3_pid)
        if process3.status() != "running" or process3.status() == "zombie":
            print_log("必要进程没在运行。。。自动杀死所有Ginthon进程。。。", process3_pid)
            # pid
            kill_pid_process(process1_pid)
            kill_pid_process(process2_pid)
            kill_pid_process(process3_pid)
            # parent_pid
            process = psutil.Process(process3_pid)
            kill_pid_process(process.ppid())
            pass
        else:
            print_log("必要进程正常运行。。。", process3_pid, process3.is_running(), process3.status())
        pass
    do_time_interval(4, do_pid_killer, tag, {})
    #
    pass

# 检测process是否可用
process1_pid = 0
process2_pid = 0
process3_pid = 0
def watch_processes(_process1_pid, _process2_pid, _process3_pid):
    global process1_pid
    process1_pid = _process1_pid
    global process2_pid
    process2_pid = _process2_pid
    global process3_pid
    process3_pid = _process3_pid
    print_log("🚩检测进程：watch_processes：", [process1_pid, process2_pid, process3_pid])
    #
    if _process1_pid > 0 and _process2_pid > 0 and _process3_pid > 0 :
        # 创建线程
        t1 = threading.Thread(target=watch_pid)
        # 启动线程
        t1.start()
        # 等待线程结束
        t1.join()
    else:
        print("❌ watch_processes：pid参数不全")
    pass