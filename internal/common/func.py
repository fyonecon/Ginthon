# -*- coding: utf-8 -*-

# 公用函数
import base64
import os
import sys
import tomllib
import random
import string
import hashlib
import platform
import re
import locale

from datetime import datetime, timezone, timedelta
from pathlib import Path

from internal.common.kits.FILETYPE_DICT import FILETYPE_Dict
from internal.common.kits.secret_aes import aes_encrypt, aes_decrypt
from internal.common.translate import lang_dict
from internal.config import get_config
from urllib.parse import urlparse, quote, unquote

# 时区
utc = timezone(timedelta(hours=8))

# test
def test(txt):
    print("公用函数test()：" + txt)
    return txt

# 打印控制台信息
def print_log(*args):
    debug = get_config("sys", "debug") # True False
    if debug:
        print(args)
    else:
        pass
    pass

# 时间日期
def get_date(format="%Y-%m-%d %H:%M:%S %p %A %B"):
    return datetime.now(utc).strftime(format)

# 秒时间戳转日期格式
def time_s_to_date(format="%Y-%m-%d %H:%M:%S %p %A %B", time_s=0):
    return datetime.fromtimestamp(time_s).strftime(format)

# 获取纳秒时间
def get_time_ns():
    return int(datetime.now(utc).timestamp() * 1000 * 1000 * 1000)

# 获取毫秒时间
def get_time_ms():
    return int(datetime.now(utc).timestamp() * 1000 * 1000)

# 获取秒时间
def get_time_s():
    return int(datetime.now(utc).timestamp() * 1000)

# 获取系统首选语言
def get_sys_language(lang = ""):
    if len(lang)>=2:
        return lang
    else:
        return locale.getlocale()[0]

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
    _cache_path = cache_path() + "/" + get_config("sys", "cache_path_main_dir") # 结尾无/
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

# 取文件后缀（最后一个后缀）
# 为空或无后缀时返回""
def get_file_ext(filename):
    filename = filename.lower()
    filename = converted_path(filename)
    return os.path.splitext(filename)[1]

# 取文件名（最后一个后缀）
# 为空或无后缀时返回""
def get_file_name(filepath):
    filepath = filepath.lower()
    filepath = converted_path(filepath)
    return os.path.basename(filepath)

# 获取mimetype
def get_file_ext_mimetype(file_ext):
    if FILETYPE_Dict.get(file_ext):
        return FILETYPE_Dict[file_ext]
    else:
        return "application/octet-stream"

# 获取当前平台存储程序缓存的路径，结尾无/
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

# 转路径的反斜杠，并删除最后一位是 /
def converted_path(path:str):
    path = path.replace('\\', '/')
    path = re.sub(r'\\+', '/', path)
    path = path.replace('//', '/')
    if path.endswith('/'):
        path = path[:-1]  # 移除最后一位 /
        pass
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
    return url_encode(aes_encrypt(txt, str_to_bytes(truncate_string(key, 16))))

# 字符串解密
def str_decode(txt_decoded, key="25nian11y21rzhw22dian27"):
    return aes_decrypt(url_decode(txt_decoded), str_to_bytes(truncate_string(key, 16)))

# md5
def md5(txt):
    return hashlib.md5(txt.encode("utf-8")).hexdigest()

# url_encode
def url_encode(text:str):
    return quote(text, encoding='utf-8')

# url_decode
def url_decode(text_encoded:str):
    return unquote(text_encoded, encoding='utf-8')

# base64_encode
def base64_encode(text: str):
    text_bytes = text.encode('utf-8')  # 先转为bytes
    return base64.b64encode(text_bytes)

# base64_decode
def base64_decode(text_encoded: str):
    decoded_bytes = base64.b64decode(text_encoded)
    return decoded_bytes.decode('utf-8')

# unicode_encode
def unicode_encode(text, encoding_type='utf-8', escape_format='python'):
    """
    encoding_type: 编码格式，可选 'utf-8', 'ascii'
    escape_format: 转义格式，可选 'html', 'url', 'hex'
    返回:
    编码后的字符串
    """
    # 编码为字节
    try:
        encoded_bytes = text.encode(encoding_type, errors='ignore')
    except LookupError:
        raise ValueError(f"不支持的编码格式: {encoding_type}")

    # 根据转义格式处理
    if escape_format == 'html':
        # HTML实体编码（&#xXXXX;）
        result = ''.join(f'&#x{ord(char):04x};' if ord(char) > 127 else char for char in text)
    elif escape_format == 'url':
        # URL百分比编码
        from urllib.parse import quote
        result = quote(text)
    elif escape_format == 'hex':
        # 纯十六进制表示
        result = encoded_bytes.hex()
    else:
        raise ValueError(f"不支持的转义格式: {escape_format}")
    return result

# unicode_decode
def unicode_decode(encoded_text, encoding_type='utf-8', escape_format='html'):
    """
    encoding_type: 编码格式，可选 'utf-8', 'ascii'
    escape_format: 转义格式，可选 'html', 'url', 'hex'
    返回:
    解码后的原始字符串
    """
    import re
    import base64
    from urllib.parse import unquote

    if escape_format == 'html' or escape_format == 'xml':
        # HTML/XML实体解码
        def html_entity_decode(match):
            entity = match.group(0)
            if entity.startswith('&#x'):
                # 十六进制实体 &#xXXXX;
                hex_code = entity[3:-1]
                return chr(int(hex_code, 16))
            elif entity.startswith('&#'):
                # 十进制实体 &#DDDD;
                dec_code = entity[2:-1]
                return chr(int(dec_code))
            else:
                # 命名实体
                html_entities = {
                    '&lt;': '<',
                    '&gt;': '>',
                    '&amp;': '&',
                    '&quot;': '"',
                    '&apos;': "'"
                }
                return html_entities.get(entity, entity)
        pattern = r'&#x[0-9a-fA-F]{1,6};|&#\d{1,6};|&[a-zA-Z]+;'
        return re.sub(pattern, html_entity_decode, encoded_text)
    elif escape_format == 'url':
        # URL解码
        return unquote(encoded_text)
    elif escape_format == 'hex':
        # 十六进制解码
        bytes_data = bytes.fromhex(encoded_text)
        return bytes_data.decode(encoding_type)
    else:
        # 直接使用指定编码解码
        return encoded_text.encode('latin-1').decode(encoding_type)

#
def back_500_data():
    return f"""
        <html style="background-color: rgba(115,115,115,0.2);">
        <head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0, user-scalable=0" /><title>500</title></head>
        <body style="background-color: transparent;">
            <h4>500</h4>
        </body>
        </html>
    """

#
def back_404_data():
    return f"""
        <html style="background-color: rgba(115,115,115,0.2);">
        <head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0, user-scalable=0" /><title>404</title></head>
        <body style="background-color: transparent;">
            <h4>404</h4>
        </body>
        </html>
    """

#
def back_404_data_html(msg):
    return f"""
        <html style="background-color: rgba(115,115,115,0.2);">
        <head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0, user-scalable=0" /><title>html 404</title></head>
        <body style="background-color: transparent;">
            <h4>html 404</h4>
            <p style="color: red;overflow: hidden;word-wrap: break-word;overflow-wrap: break-word;">{msg}</p>
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
        <html style="background-color: rgba(115,115,115,0.2);">
        <head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0, user-scalable=0" /><title>file 404</title></head>
        <body style="background-color: transparent;">
            <h4>file 404</h4>
            <p style="color: red;overflow: hidden;word-wrap: break-word;overflow-wrap: break-word;">{msg}</p>
        </body>
        </html>
    """

# 获取翻译
def get_translate(key="", lang=""):
    # 将语言转换成可用的数组索引标记
    def make_lang_index(_language):
        if len(_language) >= 2:
            _language = _language.lower()
            pass
        #
        if _language.find("zh", 0)==0 or _language.find("chinese", 0)==0:  # 简体中文（包含繁体）
            return "zh"
        elif _language.find("en", 0)==0 or _language.find("english", 0)==0:  # 英文
            return "en"
        elif _language.find("jp", 0)==0:  # 日文
            return "jp"
        elif _language.find("fr", 0)==0:  # 法语
            return "fr"
        elif _language.find("de", 0)==0:  # 德语
            return "de"
        elif _language.find("ru", 0)==0:  # 俄语或乌克兰语
            return "ru"
        elif _language.find("es", 0)==0:  # 西班牙语
            return "es"
        elif _language.find("vi", 0)==0:  # 越语
            return "vi"
        else:  # 默认英文
            return "en"
        pass
    # 系统语言
    def sys_language(_lang=""):
        if len(_lang) >= 2:
            return _lang
        else:
            sys_lan = locale.getlocale()[0]
            if sys_lan is None:
                return ""
            else:
                return sys_lan
        pass

    print("sys_language(lang)=", sys_language(lang),  locale.getlocale())
    # 索引
    lang_index = make_lang_index(sys_language(lang))
    #
    if lang_dict.get(key):
        if lang_dict[key].get(lang_index):
            return lang_dict[key][lang_index]
        else:
            if len(lang_dict["_null"][lang_index])>=1:
                return lang_dict["_null"][lang_index]
            else:
                return lang_dict["_null"]["en"]
    else:
        if lang_dict["_null"].get(lang_index):
            return lang_dict["_null"][lang_index]
        else:
            return lang_dict["_null"]["en"]
    pass

# 将size转成可读size
def format_file_size(size_bytes=0):
    if size_bytes == 0:
        return "0 B"
    # 1024进制单位
    units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
    # 找出合适的单位
    unit_index = 0
    size = float(size_bytes)
    #
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1
    pass
    return f"{size:.2f} {units[unit_index]}"
