
# 配置信息
def get_config(tag=""):
    return {
        "app": {
            "app_name": "Ginthon",
            "app_version": "1.2.0",  # 1.0.0
            "app_class": "ginthon_tray_",
            "author": "fyonecon",
            "github": "https://github.com/fyonecon/Ginthon",
            "docs": "http://datathink.top/#route=ginthon&ap=",
        },
        "sys": {
            "cache_path_main_dir": "top.datathink.Ginthon", # 缓存主目录名，默认 top.datathink.Ginthon
            "running_id_filename": "tray_running_id.cache", #
            "debug": False,  # True False
        },
        "check": {
            "min_cpu_cores": 2,  # 物理核心数
            "min_ram": 1,  # GB
            "min_python_version": (3, 12),  # 默认最低(3, 12)，即3.12.0
        },
        "flask": {
            "port": 9100,  # 服务端口 9100
        },
        "pytray": {
            "icon": "./frontend/launcher.png", # 状态栏托盘图标
            "debug": False,  # True False
        },
    }