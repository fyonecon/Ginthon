# Ginthon Tray主入口
# 代码习惯基于Golang。
from internal.app.tray.tray_create import tray_create

# main
# 运行新项目前请先：【设置.venv虚拟环境】+【初始化项目依赖pip install -r requirements.txt】
if __name__ == "__main__":
    tray_create()
    print("\n===Main-Tray-Over===\n")
    pass