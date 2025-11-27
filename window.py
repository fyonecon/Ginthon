# Ginthon Window主入口
# 代码习惯基于Golang。

from internal.bootstrap.init_sys import init_sys

# main
# 运行新项目前请先：【设置.venv虚拟环境】+【初始化项目依赖pip install -r requirements.txt】
if __name__ == "__main__":
    init_sys()
    print("\n===Main-Window-Over===\n")
    pass