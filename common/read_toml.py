import tomllib

from common.func import print_log


# 读取系统配置文件
def read_toml_config(file_path, tag):
    # 读取toml配置文件
    with open(file_path, "rb") as f:
        config_data = tomllib.load(f)
    #
    print_log("🔴 config.toml = ", tag)
    return config_data