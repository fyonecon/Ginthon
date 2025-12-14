import shutil
import os

from internal.common.func import has_file, get_platform

# 移动tray文件
def tray_file_move():
    # 兼容处理
    plt = get_platform()
    if plt == "mac" or plt == "linux":
        file = "./dist/Tray"  # 源文件路径
        pass
    else:
        file = "./dist/Tray.exe"  # 源文件路径
        pass
    # 目标文件夹路径
    new_dir = "./frontend/tray/"
    # 确保目标文件夹存在
    os.makedirs(new_dir, exist_ok=True)
    if has_file(file):
        # 构建目标文件路径
        target_file = os.path.join(new_dir, os.path.basename(file))
        # 移动文件
        shutil.move(file, target_file)
        print(f"文件已从 {file} 移动到 {target_file}")
        pass
    else:
        print("tray文件不存在=", file)
        pass
    pass

#
tray_file_move()
