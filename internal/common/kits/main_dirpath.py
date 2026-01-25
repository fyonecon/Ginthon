# -*- coding: utf-8 -*-

import sys
import os

from internal.common.func import func
from internal.config import get_config

class main_dirpath:

    # 获取虚拟环境或真实环境的相对动态路径
    # 针对打包的静态资源比如frontend文件夹
    @staticmethod
    def virtual_dirpath(sub_path_name="frontend"):
        """获取打包后资源的绝对路径"""
        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")
        return func.converted_path(os.path.join(base_path, sub_path_name))  # 返回的路径结尾无/

    # 本地缓存真实路径,结尾无/
    @staticmethod
    def cache_dirpath():
        return func.get_local_cache_path()

    # 本地数据真实路径,结尾无/
    @staticmethod
    def data_dirpath(sub_path_name=""):
        return func.get_local_data_path(sub_path_name)

    #
    pass



# 获取前端资源路径
# frontend_dir = main_dirpath.virtual_dirpath("frontend")
# print(f"资源目录: {frontend_dir}")
# cache_dir = main_cache_dirpath("log")
# print(f"缓存目录: {cache_dir}")
