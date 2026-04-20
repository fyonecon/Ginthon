# -*- coding: utf-8 -*-

# 配置信息
# 获取get_config(group="", key="")
GLOBAL_CONFIG_DICT = {
    "app": {
        "app_name": "GinthonDemo",
        "app_class": "GinthonDemo_", # 必须为string，且必须唯一，推荐使用英文
        "app_rights":  "Datathink.Top ApacheV2",
        "app_version": "1.9.6",  # 版本格式 1.0.0
        "author": "fyonecon",
        "github": "github.com/fyonecon/Ginthon",
    },
    "sys": {
        "app_state_start_time": 20260301010101, # 最早时间 YmdHis
        "app_state_end_time": 20360301010101, #  截止时间，一个版本：10年。（这是软件及扩展更新的要求）
        "cache_path_name": "top.datathink.GinthonDemo", # 缓存主目录名，默认 top.datathink.GinthonDemo ，结尾无/
        "data_path_name": "top.datathink.GinthonDemo", # 数据持久化主目录名，默认 top.datathink.GinthonDemo，结尾无/
        "data_path_names_array": [ # 系统数据持久化一级目录
            "running", "local_database", "flask_ssl", "user",  # 必要目录
            # 其它
        ],
        "running_id_filename": "running_id.cache", #
        "debug": False, # True False ，显示终端日志
    },
    "check": { # check_sys
        "min_vcpu_cores": 2,  # vCPU
        "min_ram": 1,  # GB
        "min_python_version": (3, 14),  # 默认最低(3, 14)，即3.12.0
    },
    "flask": { # web
        "white_hosts": [
            "http://127.0.0.1",
            "https://127.0.0.1",
            # 其它Host。如果需要对外暴露自定义域名，请使用Nginx反向代理127。
			"http://api.datathink.top",
			"https://api.datathink.top",
        ], #白名单域名或IP，格式：协议+IPv4+port、协议+域名
        "port": 9750,  # 服务端口 9750（前端端口使用了 9770 ，请勿重复）
        "ssl": True, # True False。开启flask自签https证书，view_url请开启https。pywebview与flask ssl一起开启或关闭。
        "debug": False,  # True False
    },
    "pywebview": { # window
        "view_url": "https://127.0.0.1:9750/view", # 生产环境：视图网址（协议+网址+端口+路径，如：http(s)://127.0.0.1:port/view ）
        "dev_url": "http://localhost:9770/view", # 开发环境：页面地址。http://localhost:9770、 http://localhost:9770/view  (此端口可在vite.config.js里面改)
        "api_host": "https://127.0.0.1:9750", # api主网址（协议+网址+端口+路径，如：http(s)://127.0.0.1:port ）
        "secret_key": "2025nian11yue21rizhouwu22dian23", # 密钥, len>=16
        "ssl": True,  # True False。pywebview与flask ssl一起开启或关闭。
        "debug": True,  # True False 打开webkit console控制台
    },
    "pytray": {
        "api_url": "https://127.0.0.1:9750/api/tray",
        "icon": "./frontend/icon.png", # 状态栏托盘图标（仅在生成二进制图片时使用）
        "debug": False,  # True False
    },
    "mysql1": {
        "ipv4": "127.0.0.1:3306",  # ip:port
        "db_name": "test_db",
        "db_user": "root2",
        "db_pwd": "",
    },
}

# =========================================================

# 读取配置信息
def get_config(group="", key=""):
    if GLOBAL_CONFIG_DICT.get(group):
        return GLOBAL_CONFIG_DICT[group][key]
    else:
        return GLOBAL_CONFIG_DICT
