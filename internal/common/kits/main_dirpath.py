import sys
import os
from pathlib import Path

from internal.common.func import cache_path, converted_path
from internal.config import get_config


# 获取虚拟环境或真实环境的相对动态路径
# 针对打包的静态资源比如frontend文件夹
def mian_virtual_dirpath(sub_path="frontend"):
    """获取打包后资源的绝对路径"""
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return converted_path(os.path.join(base_path, sub_path)) # 返回的路径结尾无/

# 缓存真实路径
def main_cache_dirpath(sub_path="running"):
    _cache_path = cache_path() + "/" + get_config("sys", "cache_path_main_dir")  # 结尾无/
    return _cache_path+"/"+sub_path

# 获取前端资源路径
# frontend_dir = mian_virtual_dirpath("frontend")
# print(f"资源目录: {frontend_dir}")
# cache_dir = main_cache_dirpath("log")
# print(f"缓存目录: {cache_dir}")
