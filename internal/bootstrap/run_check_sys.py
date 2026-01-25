# -*- coding: utf-8 -*-

import platform
import socket
import sys
import psutil

from internal.config import get_config
from internal.common.func import func

#
CONFIG = {}

# 检查最小系统版本
def check_min_sys_version():
    _sys = func.get_platform()
    if _sys == "win":
        def min_win_version():
            min_win = 10
            version_info = platform.win32_ver()
            release = version_info[0]  # 获取发布版本
            if release:
                try:
                    # 将版本号转换为整数进行比较
                    major_version = int(release.split('.')[0])
                    if major_version >= min_win:
                        return True
                    else:
                        print("最小Windows是：" + str(min_win))
                        return False
                except (ValueError, IndexError):
                    return False
            else:
                return False
        return min_win_version()
    elif _sys == "mac":
        def min_mac_version():
            min_mac = 12
            try:
                mac_version = platform.mac_ver()[0]
                if mac_version:
                    version_parts = mac_version.split('.') # 解析版本号，如 "12.6.1"
                    major_version = int(version_parts[0]) # 获取主要版本号
                    if major_version >= min_mac:
                        return True
                    else:
                        print("最小macOS是：" + str(min_mac))
                        return False
                else:
                    return False
            except (ValueError, IndexError) as e:
                return False
        return min_mac_version()
    else:
        print("当前仅支持Window10+、macOS12+。")
        return False

# 检查端口是否被占用，true已占用
def check_port_occupied(host="127.0.0.1", port=9750, timeout=2):
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
    # 读取配置信息
    global CONFIG
    CONFIG = get_config("", "")

    # 检查缓存目录，不存在就立即创建该目录
    data_path_names_array = CONFIG["sys"]["data_path_names_array"]
    for name in data_path_names_array:
        func.create_data_dir_level_1(name)
        pass

    # 至少物理双核
    cpu_count = psutil.cpu_count(logical=False)

    # 至少1GB RAM
    ram = psutil.virtual_memory()
    total_ram = ram.total / (1024 ** 3)  # 转换为 GB

    # 最小Python版本
    _python_version = platform.python_version()

    # 最下系统版本
    sys_state = check_min_sys_version()

    # 检测强制更新时间（这是软件及扩展更新的要求）
    start_time = CONFIG["sys"]["app_state_start_time"]
    end_time = CONFIG["sys"]["app_state_end_time"]
    now_time = int(func.get_date("%Y%m%d%H%M%S"))
    time_state = (now_time >= start_time) and (now_time <= end_time)

    # 判断端口是否被占用
    flask_port = CONFIG["flask"]["port"]
    flask_port_state = check_port_occupied('127.0.0.1', flask_port, timeout=2)
    if flask_port_state:
        flask_port_txt = "端口被占用：" + str(flask_port)
        pass
    else:
        flask_port_txt = "端口可用"
        pass

    # 校验可用状态
    state = cpu_count >= CONFIG["check"]["min_cpu_cores"] and total_ram >= CONFIG["check"]["min_ram"] and sys.version_info >= CONFIG["check"]["min_python_version"] and (not flask_port_state) and sys_state and time_state
    if state:
        msg = "### 系统基础状态 => "
        pass
    else:
        msg = "XXX 系统基础状态 => "
        pass

    #
    print(msg, [str(cpu_count) + " Cores", str(total_ram) + " GB", _python_version, flask_port_txt], str(now_time))
    return state