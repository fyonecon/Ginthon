# -*- coding: utf-8 -*-

import psutil
import threading

from internal.common.func import print_log

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
                print(f"### 杀死子进程 {child.pid}")
            except:
                pass
        parent.kill()
        print(f"### 杀死主进程 {_ppid}")
    except psutil.NoSuchProcess:
        print("XXX 进程已不存在")
