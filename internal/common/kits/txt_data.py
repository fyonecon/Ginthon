# -*- coding: utf-8 -*-

import os.path

from internal.common.func import func
from internal.config import get_config

#
CONFIG = get_config("", "")
txt_path = func.get_local_data_path("running")+"/" # /结尾

#
class txt_data:

    # 写txt文件
    # txt_filename文件格式：xxx.txt。model:"w"覆盖，"a"尾部追加（\n）
    @staticmethod
    def write(txt_filename, txt_content, model="w"):
        the_file = txt_path + CONFIG["app"]["app_class"] + txt_filename
        if not os.path.exists(txt_path):
            os.makedirs(txt_path, exist_ok=True)
            pass
        if model in ["w", "a"]:
            with open(the_file, model, encoding="utf-8") as file:
                file.write(txt_content)
            return True
        else:
            return False

    # 读txt文件
    @staticmethod
    def read(txt_filename):
        the_file = txt_path + CONFIG["app"]["app_class"] + txt_filename
        txt_content = ""
        if os.path.exists(the_file):  # 存在文件或文件夹
            if os.path.isfile(the_file):  # 是文件
                with open(the_file, "r", encoding="utf-8") as file:
                    txt_content = file.read()
                    pass
            else:
                pass
        else:
            pass
        return txt_content

    # 删txt文件
    @staticmethod
    def remove(txt_filename):
        the_file = txt_path + CONFIG["app"]["app_class"] + txt_filename
        if os.path.exists(the_file):  # 存在文件或文件夹
            if os.path.isfile(the_file):  # 是文件
                os.remove(the_file)
                return True
            else:
                return False
        else:
            return False

    #
    pass

