# -*- coding: utf-8 -*-

import os
import shutil

import py7zr

from internal.common.func import func

class _7z:

    # 解压整个7z文件
    # output_dirpath结尾无/
    @staticmethod
    def unarchive(archive_file, output_dirpath):
        if func.has_file(archive_file):
            with py7zr.SevenZipFile(archive_file, mode='r') as z:
                z.extractall(output_dirpath)
            return True, "7z解压完成：" + output_dirpath
        else:
            return False, "7z文件不存在：" + archive_file

    # 删除文件夹
    @staticmethod
    def remove_dir(output_dirpath):
        try:
            if os.path.exists(output_dirpath):
                shutil.rmtree(output_dirpath)
                return True, "文件夹成功删除"
            else:
                return False, "文件夹不存在：" + output_dirpath
        except PermissionError:
            return False, "删除权限不足"
        except Exception as e:
            return False, "删除文件夹出错"

    #
    pass


