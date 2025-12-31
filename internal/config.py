# -*- coding: utf-8 -*-

# 配置信息
# 获取get_config(key="")
GLOBAL_CONFIG_DICT = {
    "app": {
        "app_name": "Ginthon",
        "app_version": "1.6.4",  # 1.0.0
        "app_class": "ginthon_window_",
        "author": "fyonecon",
        "github": "https://github.com/fyonecon/Ginthon",
        "docs": "http://datathink.top/#route=ginthon&ap=",
    },
    "sys": {
        "app_state_start_time": 20251231010101, # 最早时间 YmdHis
        "app_state_end_time": 20341201010101, #  截止时间，一个版本：9年。（这是软件及扩展更新的要求）
        "cache_path_main_dir": "top.datathink.Ginthon", # 缓存主目录名，默认 top.datathink.Ginthon ，结尾无/
        "data_path_main_dir": "top.datathink.Ginthon", # 数据持久化主目录名，默认 top.datathink.Ginthon，结尾无/
        "data_path_dirs_name": [ # 系统数据持久化一级目录
            "running", "log", "local_database", "flask_ssl", "user",  # 必要
            # 其它
        ],
        "running_id_filename": "running_id.cache", #
        "debug": False,  # True False
    },
    "check": { # check_sys
        "min_cpu_cores": 2,  # 物理核心数
        "min_ram": 1,  # GB
        "min_python_version": (3, 12),  # 默认最低(3, 12)，即3.12.0
    },
    "flask": { # web
        "white_hosts": [
            "http://127.0.0.1",
            "https://127.0.0.1",
        ], #白名单域名或IP，格式：协议+IPv4+port、协议+域名
        "port": 9750,  # 服务端口 9750（前端端口使用了 9770 ，请勿重复）
        "ssl": True, # True False。开启flask自签https证书，view_url请开启https。pywebview与flask ssl一起开启或关闭。
        "debug": False,  # True False
    },
    "pywebview": { # window
        "view_url": "https://127.0.0.1:9750", # 生产环境：api主网址或视图网址（协议+网址+端口+路径，如：http(s)://127.0.0.1:port ）
        "view_class": "svelte", # 视图使用的模板（影响flask服务器加载页面）。 "vue"、"svelte"、单页填""
        "view_file_html": "view/svelte/dist", # 生产环境：pnpm run build后的dist目录。 "view/vue/dist"、"view/svelte/dist"、单页应用""。结尾无/。
        "dev_url": "http://localhost:9770/", # 开发环境：页面地址，默认 http://localhost:9770/ (此端口可在vite.config.js里面改)
        "secret_key": "2025nian11yue21rizhouwu22dian23", # 密钥, len>=16
        "ssl": True,  # True False。pywebview与flask ssl一起开启或关闭。
        "debug": True,  # True False
    },
    "pytray": {
        "api_url": "http://127.0.0.1:9750/api/tray",
        "icon": "./frontend/icon.png", # 状态栏托盘图标
        "debug": False,  # True False
    },
    "mysql1": {
        "ipv4": "127.0.0.1:3306",  # ip:port
        "db_name": "test_db",
        "db_user": "root2",
        "db_pwd": "",
    },
}

# 读取配置信息
def get_config(group="", key=""):
    if GLOBAL_CONFIG_DICT.get(group):
        if GLOBAL_CONFIG_DICT[group].get(key):
            return GLOBAL_CONFIG_DICT[group][key]
        else:
            return GLOBAL_CONFIG_DICT[group]
    else:
        return GLOBAL_CONFIG_DICT
