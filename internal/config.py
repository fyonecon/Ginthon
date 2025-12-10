# 配置信息
# 获取get_config(key="")
GLOBAL_CONFIG_DICT = {
    "app": {
        "app_name": "Ginthon Tray",
        "app_version": "1.4.4",  # 1.0.0
        "app_class": "ginthon_tray_",
        "author": "fyonecon",
        "github": "https://github.com/fyonecon/Ginthon",
        "docs": "http://datathink.top/#route=ginthon&ap=",
    },
    "sys": {
        "cache_path_main_dir": "top.datathink.Ginthon", # 缓存主目录名，默认 top.datathink.Ginthon
        "running_id_filename": "running_id.cache", #
        "debug": False,  # True False
    },
    "check": {
        "min_cpu_cores": 2,  # 物理核心数
        "min_ram": 1,  # GB
        "min_python_version": (3, 12),  # 默认最低(3, 12)，即3.12.0
    },
    "flask": {
        "white_hosts": ["http://127.0.0.1", "https://127.0.0.1", "http://datathink.top", "https://datathink.top"],  # 白名单域名或IP，格式：协议+IPv4+port、协议+域名
        "port": 9750,  # 服务端口 9750
        "debug": False,  # True False
    },
    "pywebview": {
        "url": "http://127.0.0.1:9750/api/tray",  # 网址（协议+网址+端口+路径，如：http://127.0.0.1:9750/? ）
        "secret_key": "2025nian11yue21rizhouwu22dian23",  # 密钥, len>=16
        "ssl": False,  # True False
        "debug": False,  # True False
    },
    "pytray": {
        "icon": "./frontend/launcher.png", # 状态栏托盘图标
        "debug": False,  # True False
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