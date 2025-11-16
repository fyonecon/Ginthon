
import psutil
import platform
import sys
import socket

from common.global_data import GlobalData

# 检查端口是否被占用
def check_port_occupied(host="127.0.0.1", port=9100, timeout=2):
    try:
        # 创建 socket 对象
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            # 尝试连接
            result = sock.connect_ex((host, port))
            # 如果返回 0，表示连接成功，端口被占用
            return result == 0
    except socket.gaierror:
        return False
    except Exception as e:
        return False

# 检测系统，硬性条件
def check_sys(tag):
    print("SYS Checking...", tag)
    # 至少物理双核
    cpu_count = psutil.cpu_count(logical=False)
    # 至少1GB RAM
    ram = psutil.virtual_memory()
    total_ram = ram.total / (1024 ** 3)  # 转换为 GB
    # 最小Python版本
    _python_version = platform.python_version()
    # 判断端口是否被占用
    flask_port = GlobalData["flask"]["port"]
    flask_port_state = check_port_occupied('127.0.0.1', flask_port, timeout=2)
    #
    print("✅SYS=>", "\n", [str(cpu_count)+" Cores", str(total_ram)+" GB", _python_version, flask_port_state], "\n")
    return cpu_count >= GlobalData["min_cpu_cores"] and total_ram >= GlobalData["min_ram"] and sys.version_info >= GlobalData["min_python_version"] and (not flask_port_state)