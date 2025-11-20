
# 配置信息
def get_config(tag):
    return {
        "app": {
            "app_name": "Ginthon",
            "app_version": "1.1.0",  # 1.0.0
            "app_class": "ginthon_",
            "author": "fyonecon",
            "github": "https://github.com/fyonecon/Ginthon",
            "docs": "http://datathink.top/#route=ginthon&ap=",
        },
        "sys": {
            "cache_path_main_dir": "top.datathink.Ginthon", # 缓存主目录名，默认 top.datathink.Ginthon
            "debug": False,  # True False
        },
        "check": {
            "min_cpu_cores": 2,  # 物理核心数
            "min_ram": 1,  # GB
            "min_python_version": (3, 12),  # 默认最低(3, 12)，即3.12.0
        },
        "flask": {
            "port": 9100,  # 服务端口 9100
            "debug": False,  # True False
        },
        "pywebview": {
            "url": "http://127.0.0.1:9100/?", # 网址（协议+网址+端口+路径，如：http://127.0.0.1:9100/? ）
            "ssl": False,  # True False
            "debug": False,  # True False
        },
        "pystray": {
            "icon": "./frontend/launcher.png", # 状态栏托盘图标
        },
        "mysql1": {
            "ipv4": "127.0.0.1:3306",  # ip:port
            "db_name": "test_db",
            "db_user": "root2",
            "db_pwd": "",
        },
    }