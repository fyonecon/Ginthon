import os

from internal.common.func import converted_path, url_decode
from internal.common.kits.local_database import local_database_get_data
from internal.common.request_input import request_input

#


# 获取当前dir下的文件或目录
def get_play_audio_list(request):
    _now_dir = request_input(request, "now_dir")

    # 转换地址格式
    now_dir = converted_path(_now_dir)

    # 目标地址
    list_dirs = []
    list_files = []
    root_paths = []

    # 读取文件列表
    if len(now_dir) > 0:  # 有值就读取该目录
        try:
            # 读文件夹
            with os.scandir(now_dir) as entries:
                for entry in entries:
                    if entry.is_file():
                        if entry.name.find(".") == 0:  # 排除
                            pass
                        else:
                            list_files.append(entry.name)
                            pass
                        print(f"文件: {entry.name}", entry)
                    elif entry.is_dir():
                        if entry.name.find(".") == 0:  # 排除
                            pass
                        else:
                            list_dirs.append(entry.name)
                            pass
                        print(f"文件夹: {entry.name}", entry)
                    pass
                pass
            pass
            state = 1
            msg = "OK"
        except:
            state = 1  # 1
            msg = "Null"
            pass
        pass
    else:  # 无值就展示已经设置的所有目录
        play_audio_list_dir_key = "play_audio_list_dirs"
        _value, _state = local_database_get_data(play_audio_list_dir_key)
        if _state != -1:
            play_audio_list_dir_array = _value.split("#@")
            for the_dir in play_audio_list_dir_array:
                if len(the_dir) >= 0:  # 清除空内容
                    list_dirs.append(the_dir)
                    pass
                pass
            root_paths = list_dirs
            state = 1
            msg = "Default Set Data"
        else:
            state = 0
            msg = "Null set"
        pass
    pass

    #
    return {
        "state": state,
        "msg": msg,
        "content": {
            "list_dirs": list_dirs,
            "list_files": list_files,
            "view_path": now_dir,
            "root_paths": root_paths,
        },
    }
