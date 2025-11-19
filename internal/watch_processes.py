
import psutil
import threading

from common.func import print_log

# 按照主进程杀死所有进程
def kill_process_tree(_ppid):
    print("🔴 Ready App Exit.", " [", "主进程:", _ppid, "]")
    """杀死指定 PID 的进程以及它的所有子进程（递归）"""
    try:
        parent = psutil.Process(_ppid)
        children = parent.children(recursive=True)  # 所有子孙进程
        for child in children:
            try:
                child.kill()
                print(f"✅ 杀死子进程 {child.pid}")
            except:
                pass
        parent.kill()
        print(f"✅ 杀死主进程 {_ppid}")
    except psutil.NoSuchProcess:
        print("❌ 进程已不存在")

# 时刻准备杀掉全部进程
def ready_kill_process_pids():
    process3 = psutil.Process(process3_pid)
    # 主程
    ppid = process3.ppid()
    #=============会影响kill_process_tree()而杀不完进程============
    # 所有1级子程
    parent_process = psutil.Process(ppid)
    child_processes = parent_process.children(recursive=True)  # 所有子孙进程
    child_process_pids = []
    for child_process in child_processes:
        child_process_pid = child_process.pid
        child_process_pids.append(child_process_pid)
        pass
    #
    all_pid = child_process_pids+[ppid]
    print_log("所有进程: ", all_pid)
    #=========================================================
    #
    if process3.status() != "running" or process3.status() == "zombie":
        print_log("❌ 必要进程没在运行（自动杀死所有Ginthon进程）", process3_pid, process3.is_running(), process3.status())
        kill_process_tree(ppid)
    else:
        print_log("✅ 必要进程正常运行。。。", process3_pid, process3.is_running(), process3.status())
    #
    pass

# 检测process是否可用
process1_pid = 0
process2_pid = 0
process3_pid = 0 # 这是主要检测对象
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
        t1 = threading.Thread(target=ready_kill_process_pids)
        # 启动线程
        t1.start()
        # 等待线程结束
        t1.join()
    else:
        print("❌ watch_processes：pid参数不全")
    pass