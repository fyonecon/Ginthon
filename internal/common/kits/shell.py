import subprocess
import shutil


# 运行二进制文件
# shell_run_bin_process("/usr/bin/ls", "-la")
def shell_run_bin_process(binary_path, *args):
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
