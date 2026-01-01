# -*- coding: utf-8 -*-

import os
import signal
import psutil
import threading

class watch_processes:

    # 杀死线程
    @staticmethod
    def kill_process_by_pid(pid):
        """通过PID杀死进程"""
        try:
            # 发送SIGTERM信号（优雅终止）
            os.kill(pid, signal.SIGTERM)
            # print(f"已向进程 {pid} 发送终止信号")
            return True
        except ProcessLookupError:
            print(f"进程 {pid} 不存在")
            return False
        except PermissionError:
            print(f"权限不足，无法终止进程 {pid}")
            return False
        except Exception as e:
            print(f"终止进程 {pid} 时出错: {e}")
            return False

    # 按照主进程杀死所有进程
    @staticmethod
    def kill_process_by_tree(_ppid):
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

    #
    pass


