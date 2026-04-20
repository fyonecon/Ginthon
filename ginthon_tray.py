# -*- coding: utf-8 -*-
import sys
import io

# 修复标准输出的编码
if sys.platform == 'win32' and hasattr(sys.stdout, 'buffer'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    pass

# Ginthon Tray主入口
# 代码习惯基于Golang。
from internal.app.tray.tray_create import tray_create

# main
# 运行新项目前请先：【设置.venv虚拟环境】+【初始化项目依赖pip install -r requirements.txt】
if __name__ == "__main__":
    tray_create()
    print("\n===Main-Tray-Over===\n")
    pass