# 公用函数
import os
import sys
import tomllib
import random
import string
import hashlib
import platform
import re

from datetime import datetime, timezone, timedelta
from pathlib import Path

from internal.common.kits.secret_aes import aes_encrypt, aes_decrypt
from internal.config import get_config
from urllib.parse import urlparse

# 时区
utc = timezone(timedelta(hours=8))

# test
def test(txt):
    print("公用函数test()：" + txt)
    return txt

# 打印控制台信息
def print_log(*args):
    debug = get_config("func")["sys"]["debug"] # True False
    if debug:
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

# 获取当前main的绝对路径
def main_path():
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
# 只能创建1级子文件夹
def create_dir_level_1(dirpath):
    _cache_path = cache_path() + "/" + get_config("func")["sys"]["cache_path_main_dir"] # 结尾无/
    # 没有主文件就直接创建
    if not has_dir(_cache_path):
        os.mkdir(_cache_path)
        pass
    # 创建子文件夹
    full_path = _cache_path+"/"+dirpath
    # print("create_dir_level_1=", _cache_path, full_path)
    if not has_dir(full_path): # 不存在
        os.mkdir(full_path)
        return True, full_path
    else: # 已存在
        return True, full_path

# 读取系统配置文件
def read_toml_config(file_path, tag):
    # 读取toml配置文件
    if has_file(file_path):
        with open(file_path, "rb") as f:
            config_data = tomllib.load(f)
        return config_data
        pass
    else:
        return ""
    pass

# 获取系统类型: win mac linux
def get_platform():
    # 判断具体系统类型
    if sys.platform.startswith('win'):
        return "win"
    elif sys.platform.startswith('linux'):
        return "linux"
    elif sys.platform.startswith('darwin'):
        return "mac"
    # elif sys.platform.startswith('cygwin'):
    #     return "cygwin"
    else: # 其他平台
        return sys.platform

# 获取平台是x86还是arm的cpu
def get_machine():
    machine = platform.machine()
    if machine == 'arm64' or machine == 'ARM64':
        return "arm"
    elif machine == 'x86_64' or machine == 'AMD64' or machine == 'amd64':
        return "x86"
    else:
        return "null-cpu"

# 获取当前平台存储程序缓存的路径
def cache_path():
    p = get_platform()
    if p == "win":
        localappdata = os.environ.get("LOCALAPPDATA", "")
        local_path = Path(localappdata)
        return converted_path(str(local_path))
    elif p == "linux":
        xdg_cache_home = Path(os.environ.get('XDG_CACHE_HOME', Path.home() / '.cache'))
        return str(xdg_cache_home)
    elif p == "mac":
        user_cache_dir = Path.home() / "Library" / "Caches"
        return str(user_cache_dir)
    else: # 其他平台
        return ""

# 转路径的反斜杠
def converted_path(path:str):
    path = path.replace('\\', '/')
    path = re.sub(r'\\+', '/', path)
    return path

# 是否是网址
def is_url(url):
    try:
        result = urlparse(url)
        # 检查必要的组件
        if not all([result.scheme, result.netloc]):
            return False
        # 检查协议否有效
        if result.scheme not in ['http', 'https', 'ftp', 'ftps']:
            return False
        # 检查网络位置（域名或IP）
        if not result.netloc:
            return False
        return True
    except Exception:
        return False

# string 转 bytes
def str_to_bytes(txt: str):
    return txt.encode("utf-8")

# 截取固定长度的字符串，从第1位
def truncate_string(text, length):
    if len(text) <= length:
        return text
    return text[:length]

# 生成指定长度范围内的随机字母数字字符串
def rand_range_string(min_length, max_length):
    length = random.randint(min_length, max_length)
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))

# 字符串加密
def str_encode(txt, key="25nian11y21rzhw22dian27"):
    return aes_encrypt(txt, str_to_bytes(truncate_string(key, 16)))

# 字符串解密
def str_decode(txt, key="25nian11y21rzhw22dian27"):
    return aes_decrypt(txt, str_to_bytes(truncate_string(key, 16)))

# md5
def md5(txt):
    return hashlib.md5(txt.encode("utf-8")).hexdigest()

#
def back_500_data():
    return f"""
        <html>
        <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0, user-scalable=0" /><title>500</title>
        <body>
            <h4>500</h4>
        </body>
        </html>
    """

#
def back_404_data():
    return f"""
        <html>
        <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0, user-scalable=0" /><title>404</title>
        <body>
            <h4>404</h4>
        </body>
        </html>
    """

#
def back_404_data_html(msg):
    return f"""
        <html>
        <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0, user-scalable=0" /><title>html 404</title>
        <body>
            <h4>html 404</h4>
            <p style="color: red;">{msg}</p>
        </body>
        </html>
    """

#
def back_404_data_api(msg):
    return {
        "state": 404,
        "msg": "api 404",
        "content": {
            "error": msg,
        }
    }

#
def back_404_data_file(msg):
    return f"""
        <html>
        <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0, user-scalable=0" /><title>file 404</title>
        <body>
            <h4>file 404</h4>
            <p style="color: red;">{msg}</p>
        </body>
        </html>
    """


