
# 配置信息
def get_config(tag=""):
    return {
        "app": {
            "app_name": "Ginthon",
            "app_version": "1.4.1",  # 1.0.0
            "app_class": "ginthon_window_",
            "author": "fyonecon",
            "github": "https://github.com/fyonecon/Ginthon",
            "docs": "http://datathink.top/#route=ginthon&ap=",
        },
        "sys": {
            "cache_path_main_dir": "top.datathink.Ginthon", # 缓存主目录名，默认 top.datathink.Ginthon
            "running_id_filename": "running_id.cache", #
            "debug": False,  # True False
        },
        "check": { # check_sys
            "min_cpu_cores": 2,  # 物理核心数
            "min_ram": 1,  # GB
            "min_python_version": (3, 12),  # 默认最低(3, 12)，即3.12.0
        },
        "flask": { # web
            "white_hosts": ["http://127.0.0.1", "https://127.0.0.1", "http://datathink.top", "https://datathink.top"], #白名单域名或IP，格式：协议+IPv4+port、协议+域名
            "port": 9100,  # 服务端口 9100
            "debug": False,  # True False
        },
        "pywebview": { # window
            "view_host": "http://127.0.0.1", # 视图网址（协议+网址+端口+路径，如：http://127.0.0.1 ）
            "view_class": "svelte", # 视图使用的模板（影响flask服务器加载页面）。 "vue"、"svelte"、单页填""
            "view_index.html": "/svelte/dist", # pnpm run build后的dist目录。 "/vue/dist"、"/svelte/dist"、单页应用""。结尾无/。
            "secret_key": "2025nian11yue21rizhouwu22dian23", # 密钥, len>=16
            "ssl": False,  # True False
            "debug": True,  # True False
        },
        "mysql1": {
            "ipv4": "127.0.0.1:3306",  # ip:port
            "db_name": "test_db",
            "db_user": "root2",
            "db_pwd": "",
        },
    }