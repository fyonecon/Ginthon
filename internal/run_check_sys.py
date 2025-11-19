
import platform
import socket
import sys

import psutil

from common.config import get_config
from common.func import root_path, has_dir, create_dir

#
CONFIG = {}

# 检查端口是否被占用，true已占用
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
def run_check_sys():
    # 创建必要文件夹及检查必要目录是否存在
    _root_path = root_path()
    #
    must_dir_storage = "storage"
    if not has_dir(_root_path + must_dir_storage):
        create_dir(_root_path + must_dir_storage)
        pass
    must_dir_running = "storage/running"
    if not has_dir(_root_path + must_dir_running):
        create_dir(_root_path + must_dir_running)
        pass
    must_dir_log = "storage/log"
    if not has_dir(_root_path + must_dir_log):
        create_dir(_root_path + must_dir_log)
        pass

    # 读取配置信息
    global CONFIG
    CONFIG = get_config("run_check_sys")

    # 至少物理双核
    cpu_count = psutil.cpu_count(logical=False)
    # 至少1GB RAM
    ram = psutil.virtual_memory()
    total_ram = ram.total / (1024 ** 3)  # 转换为 GB
    # 最小Python版本
    _python_version = platform.python_version()
    # 判断端口是否被占用
    flask_port = CONFIG["flask"]["port"]
    flask_port_state = check_port_occupied('127.0.0.1', flask_port, timeout=2)
    if flask_port_state:
        flask_port_txt = "端口被占用：" + str(flask_port)
        pass
    else:
        flask_port_txt = "端口可用"
        pass
    #
    state = cpu_count >= CONFIG["check"]["min_cpu_cores"] and total_ram >= CONFIG["check"]["min_ram"] and sys.version_info >= CONFIG["check"]["min_python_version"] and (not flask_port_state)
    if state:
        msg = "✅ 系统基础状态 => "
        pass
    else:
        msg = "❌ 系统基础状态 => "
        pass
    print(msg, [str(cpu_count) + " Cores", str(total_ram) + " GB", _python_version, flask_port_txt])
    return state