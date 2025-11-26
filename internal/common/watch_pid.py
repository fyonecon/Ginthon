import os
import signal

# 杀死线程
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
