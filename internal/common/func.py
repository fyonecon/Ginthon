# 公用函数
import os

from datetime import datetime, timezone, timedelta

# 时区
utc = timezone(timedelta(hours=8))

# test
def test(txt):
    print("公用函数test()：" + txt)
    return txt

# 打印控制台信息
def print_log(*args):
    debud = False # True False
    if debud:
        print(args)
    else:
        pass
    pass

# 时间日期
def get_date(format="%Y-%m-%d %H:%M:%S %p %A %B"):
    return datetime.now(utc).strftime(format)

# 获取毫秒时间
def get_time_ms():
    return datetime.now(utc).microsecond // 1000

# 获取秒时间
def get_time_s():
    return datetime.now(utc).microsecond // 1000 // 1000

# 获取当前main的绝对
def root_path():
    return os.getcwd() + "/"

# 验证当前路径的文件是否存在
def has_file(full_filepath):
    if os.path.exists(full_filepath): # 存在文件或文件夹
        if os.path.isfile(full_filepath): # 是文件
            return True
        else:
            return False
    else:
        return False

# 验证当前目录是否存在
def has_dir(full_dirpath):
    if os.path.isfile(full_dirpath):  # 是文件
        return False
    else:
        if os.path.exists(full_dirpath): # 存在文件或文件夹
            return True
        else:
            return False

# 创建文件夹（只能在main.py目录或子目录创建）,dirpath开头和结尾都不带 /
def create_dir(dirpath):
    root_path = root_path()
    full_path = root_path+dirpath
    if not has_dir(full_path): # 不存在
        os.mkdir(full_path)
        return True
    else: # 已存在
        return True