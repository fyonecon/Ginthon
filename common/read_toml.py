import tomllib

# 读取系统配置文件
def read_toml_config(tag):
    # 读取toml配置文件
    with open("./storage/toml/config.toml", "rb") as f:
        config_data = tomllib.load(f)
    #
    # print("config.toml\n", tag, config_data)
    return config_data