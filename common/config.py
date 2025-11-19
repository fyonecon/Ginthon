import sys

from common.func import root_path, has_file
from common.read_toml import read_toml_config

# 初始化
def get_config(tag):
    # 读取toml配置信息
    file_path = root_path()+"storage/toml/config.toml"
    if not has_file(file_path):
        print("❌ 配置文件不存在：", [file_path, "config.toml"])
        sys.exit(-1) # 不能存在就立即退出程序
        return {}
    else:
        TOML = read_toml_config(file_path, tag)
        #
        CONFIG = {
            ######
            "app": {
                "app_name": TOML["app"]["app_name"],
                "app_version": TOML["app"]["app_version"],  # 1.0.0
                "app_class": TOML["app"]["app_class"],
                "author": TOML["app"]["author"],
                "github": TOML["app"]["github"],
                "docs": TOML["app"]["docs"],
            },
            "sys": {
                "log_path": TOML["sys"]["log_path"],  # /结尾
                "debug": TOML["sys"]["debug"],  # True False
            },
            "check": {
                "min_cpu_cores": 2,  # 物理核心数
                "min_ram": 1,  # GB
                "min_python_version": (3, 12),  # 默认最低(3, 12)
            },
            ######
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