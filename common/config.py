from common.read_toml import read_toml_config

# 全局变量
CONFIG = {}

# 初始化
def init_config():
    global CONFIG
    # 读取toml配置信息
    file_path = "./storage/toml/config.toml"
    TOML = read_toml_config(file_path, "1")
    #
    CONFIG = {
        "app_name": TOML["app"]["app_name"],
        "app_version": TOML["app"]["app_version"],
        "app_class": TOML["app"]["app_class"],
        "author": TOML["app"]["author"],
        "docs": "http://datathink.top/#route=ginthon&ap=",
        "log_path": TOML["sys"]["log_path"],  # /结尾
        "min_cpu_cores": 2,  # 物理核心数
        "min_ram": 1,  # GB
        "min_python_version": (3, 12),  # 默认 (3, 12)
        "flask": {
            "port": TOML["flask"]["port"],  # 服务端口 9100
            "debug": TOML["flask"]["debug"],  # True False
        },
        "pywebview": {
            "ssl": TOML["pywebview"]["ssl"],  #
            "debug": TOML["pywebview"]["debug"],  # True False
        },
        "mysql1": {
            "ipv4": TOML["mysql1"]["ipv4"],  # ip:port
            "db_name": TOML["mysql1"]["db_name"],
            "db_user": TOML["mysql1"]["db_user"],
            "db_pwd": TOML["mysql1"]["db_pwd"],
        },
    }
    return CONFIG

# 读取（同线程才可读取值，否则读为空）
def read_config():
    return CONFIG