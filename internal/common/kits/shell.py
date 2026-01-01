# -*- coding: utf-8 -*-
import os
import platform
import subprocess
import shutil

class shell:

    # 打开本地文件或文件夹
    @staticmethod
    def open_in_folder(filepath=""):
        # 规范化路径
        path = os.path.normpath(filepath)
        # 检查路径是否存在
        if not os.path.exists(path):
            print(f"错误: 路径不存在 - {path}")
            return False
        #
        system = platform.system()
        try:
            if system == "Windows":
                # Windows系统 - os.startfile 可以打开文件和文件夹
                os.startfile(path)
            elif system == "Darwin":  # macOS
                # macOS - open 命令可以打开文件和文件夹
                subprocess.run(["open", path], check=True)
            elif system == "Linux":
                # Linux系统 - xdg-open 可以打开文件和文件夹
                subprocess.run(["xdg-open", path], check=True)
            else:
                print(f"错误: 不支持的操作系统 - {system}")
                return False

            print(f"成功打开: {path}")
            return True
        except Exception as e:
            print(f"打开失败: {e}")
            return False

    # 运行二进制文件
    # shell_run_bin_process("/usr/bin/ls", "-la")
    @staticmethod
    def run_bin_process(binary_path, *args):
        try:
            result = subprocess.run([binary_path] + list(args),
                                    capture_output=True,
                                    text=True,
                                    check=True)

            print(f"退出码: {result.returncode}")
            print(f"标准输出: {result.stdout}")
            if result.stderr:
                print(f"标准错误: {result.stderr}")
                pass

            return result
        except FileNotFoundError:
            print(f"错误: 文件不存在 {binary_path}")
        except subprocess.CalledProcessError as e:
            print(f"错误: 进程执行失败, 退出码: {e.returncode}")
            print(f"错误输出: {e.stderr}")
        except Exception as e:
            print(f"未知错误: {e}")
        return None

    #
    pass


