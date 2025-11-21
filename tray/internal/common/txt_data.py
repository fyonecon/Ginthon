import os.path

from tray.internal.common.func import cache_path
from tray.internal.config import get_config

#
_cache_path = cache_path() + "/" + get_config("func")["sys"]["cache_path_main_dir"] # 结尾无/
txt_path = _cache_path+"/running/" # /结尾

# 写txt文件
# txt_filename文件格式：xxx.txt。model:"w"覆盖，"a"尾部追加（\n）
def txt_write(txt_filename, txt_content, model="w"):
    the_file = txt_path + txt_filename
    if model in ["w", "a"]:
        with open(the_file, model, encoding="utf-8") as file:
            file.write(txt_content)
        return True
    else:
        return False

# 读txt文件
def txt_read(txt_filename):
    the_file = txt_path + txt_filename
    txt_content = ""
    if os.path.exists(the_file): # 存在文件或文件夹
        if os.path.isfile(the_file): # 是文件
            with open(the_file, "r", encoding="utf-8") as file:
                txt_content = file.read()
                pass
        else:
            pass
    else:
        pass
    return txt_content

# 删txt文件
def txt_remove(txt_filename):
    the_file = txt_path + txt_filename
    if os.path.exists(the_file): # 存在文件或文件夹
        if os.path.isfile(the_file): # 是文件
            os.remove(the_file)
            return True
        else:
            return False
    else:
        return False