# Ginthon Window主入口
# 代码习惯基于Golang。
import argparse
from internal.bootstrap.init_sys import init_sys

# main
# 运行新项目前请先：【设置.venv虚拟环境】+【初始化项目依赖pip install -r requirements.txt】
if __name__ == "__main__":
    # 获取运行参数
    parser = argparse.ArgumentParser(description='窗口程序')
    parser.add_argument('--cmd', type=str, help='运行模式：开发dev还是构建build')
    args = parser.parse_args()
    cmd_model = args.cmd
    print("'--cmd'=", cmd_model)
    if cmd_model == "":
        cmd_model = "dev"
        pass
    #
    if cmd_model in ["dev", "build"]:
        #
        print("'--cmd'=", cmd_model)
        init_sys(cmd_model)
        pass
    else:
        print("'--cmd' Error")
        pass
    #
    print("\n===Main-Window-Over===\n")
    pass