#!/usr/bin/env python3
"""
跨平台开发构建脚本 v3.2
step_3: 前台显示执行过程 + 后台健康检查
其他步骤: 阻塞执行，原样显示输出
"""

# -*- coding: utf-8 -*-

import json
import sys
import os
import platform
import subprocess
import shutil
import signal
import time
import requests
import threading
import select
import socket
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum


class StepStatus(Enum):
    """步骤状态枚举"""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"
    HEALTH_CHECKING = "health_checking"


@dataclass
class StepResult:
    """步骤执行结果"""
    step_name: str
    status: StepStatus = StepStatus.PENDING
    returncode: Optional[int] = None
    stdout: str = ""
    stderr: str = ""
    duration: float = 0.0
    process_pid: Optional[int] = None
    is_background: bool = False
    health_check_passed: bool = False
    skipped_reason: str = ""


@dataclass
class Config:
    """配置文件"""
    steps: Dict[str, str] = field(default_factory=dict)
    custom_commands: Dict[str, str] = field(default_factory=dict)
    health_checks: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    timeout_seconds: int = 120

    @classmethod
    def from_file(cls, filepath: str = "dev.json") -> "Config":
        """从文件加载配置"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if "steps" not in data:
                raise ValueError("配置文件中缺少 'steps' 字段")

            return cls(
                steps=data["steps"],
                custom_commands=data.get("custom_commands", {}),
                health_checks=data.get("health_checks", {}),
                timeout_seconds=data.get("timeout_seconds", 120)
            )
        except FileNotFoundError:
            print(f"❌ 配置文件 '{filepath}' 不存在")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"❌ 配置文件 JSON 格式错误: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"❌ 加载配置文件失败: {e}")
            sys.exit(1)


class CrossPlatformDevRunner:
    def __init__(self, config_file: str = "dev.json"):
        """初始化"""
        self.config = Config.from_file(config_file)
        self.os_type = platform.system().lower()
        self.is_windows = self.os_type == "windows"
        self.is_macos = self.os_type == "darwin"
        self.is_linux = self.os_type == "linux"

        # 命令映射
        self.command_map = self._init_command_map()

        # 当前工作目录
        self.original_cwd = os.getcwd()

        # 步骤结果
        self.step_results: Dict[str, StepResult] = {}

        # 后台进程列表（用于 step_3）
        self.background_processes: List[subprocess.Popen] = []

        # 超时设置
        self.timeout = self.config.timeout_seconds

        # 信号处理
        self._setup_signal_handlers()

    def _setup_signal_handlers(self):
        """设置信号处理器"""
        if not self.is_windows:
            signal.signal(signal.SIGINT, self._signal_handler)
            signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, signum, frame):
        """信号处理函数"""
        print(f"\n⚠️  收到中断信号，正在清理...")
        self._cleanup_background_processes()
        sys.exit(1)

    def _cleanup_background_processes(self):
        """清理后台进程"""
        for proc in self.background_processes:
            try:
                if proc.poll() is None:
                    proc.terminate()
                    try:
                        proc.wait(timeout=3)
                    except subprocess.TimeoutExpired:
                        proc.kill()
            except:
                pass
        self.background_processes.clear()

    def _init_command_map(self) -> Dict[str, str]:
        """初始化命令映射表"""
        default_commands = {
            "npm": "npm.cmd" if self.is_windows else "npm",
            "pnpm": "pnpm.cmd" if self.is_windows else "pnpm",
            "yarn": "yarn.cmd" if self.is_windows else "yarn",
            "python": "python" if self.is_windows else "python3",
            "pip": "pip" if self.is_windows else "pip3",
            "cd": "cd",
            "echo": "echo",
        }

        for cmd, custom_cmd in self.config.custom_commands.items():
            default_commands[cmd] = custom_cmd

        return default_commands

    def _log(self, message: str, level: str = "INFO", step: str = ""):
        """统一的日志输出"""
        colors = {
            "INFO": "\033[94m",
            "SUCCESS": "\033[92m",
            "ERROR": "\033[91m",
            "WARNING": "\033[93m",
            "STEP": "\033[95m",
            "HEALTH": "\033[96m",
            "SKIP": "\033[90m",
            "END": "\033[0m"
        }

        supports_color = (
                not self.is_windows or
                os.environ.get('TERM_PROGRAM') == 'vscode' or
                os.environ.get('WT_SESSION')
        )

        if supports_color and level in colors:
            prefix = f"{colors[level]}[{level}]{colors['END']}"
        else:
            prefix = f"[{level}]"

        if step:
            prefix = f"{prefix} [{step}]"

        print(f"{prefix} {message}")

    def _check_command_exists(self, command: str) -> tuple[bool, str]:
        """检查命令是否存在"""
        if command in ["cd", "echo"]:
            return True, command

        cmd = self.command_map.get(command, command)

        if shutil.which(cmd) is not None:
            return True, cmd

        if self.is_windows:
            cmd_without_ext = cmd.replace('.cmd', '').replace('.exe', '')
            if shutil.which(cmd_without_ext) is not None:
                return True, cmd_without_ext

        return False, cmd

    def _handle_cd_command(self, args: List[str]) -> bool:
        """处理cd命令"""
        if not args:
            self._log("cd 命令需要参数", "ERROR")
            return False

        target_dir = args[0]
        if not os.path.isabs(target_dir):
            target_dir = os.path.join(os.getcwd(), target_dir)

        target_dir = os.path.normpath(target_dir)

        try:
            if not os.path.exists(target_dir):
                self._log(f"目录不存在: {target_dir}", "ERROR")
                return False

            os.chdir(target_dir)
            self._log(f"切换到目录: {os.getcwd()}", "SUCCESS")
            return True
        except Exception as e:
            self._log(f"切换目录失败: {str(e)}", "ERROR")
            return False

    def _check_service_already_running(self, url: str = "http://localhost:5175/") -> bool:
        """检查服务是否已经在运行"""
        self._log(f"检查服务是否已启动: {url}", "INFO", "pre-check")

        try:
            # 首先解析URL获取端口
            from urllib.parse import urlparse
            parsed = urlparse(url)
            host = parsed.hostname or 'localhost'
            port = parsed.port or (80 if parsed.scheme == 'http' else 443)

            # 检查端口是否开放
            self._log(f"检查端口 {port} 是否开放...", "INFO", "pre-check")
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                result = sock.connect_ex((host, port))
                sock.close()

                if result != 0:
                    self._log(f"端口 {port} 未开放", "INFO", "pre-check")
                    return False
            except Exception as e:
                self._log(f"检查端口时出错: {str(e)}", "WARNING", "pre-check")
                return False

            # 尝试HTTP请求
            self._log("尝试HTTP请求...", "INFO", "pre-check")
            try:
                response = requests.get(url, timeout=3)
                if 200 <= response.status_code < 500:
                    self._log(f"✅ 服务已在运行! 状态码: {response.status_code}", "SUCCESS", "pre-check")
                    return True
                else:
                    self._log(f"⚠️  服务返回状态码: {response.status_code}", "WARNING", "pre-check")
                    return False
            except requests.exceptions.Timeout:
                self._log("HTTP请求超时", "WARNING", "pre-check")
                return False
            except requests.exceptions.ConnectionError:
                self._log("HTTP连接被拒绝", "INFO", "pre-check")
                return False
            except Exception as e:
                self._log(f"HTTP请求错误: {str(e)}", "WARNING", "pre-check")
                return False

        except Exception as e:
            self._log(f"检查服务时出错: {str(e)}", "WARNING", "pre-check")
            return False

    def _run_foreground_step(self, step_key: str, command_str: str, wait_for_completion: bool = True) -> bool:
        """运行前台步骤 - 原样显示控制台输出"""
        self._log(f"开始执行: {command_str}", "STEP", step_key)

        start_time = time.time()
        result = StepResult(step_name=step_key)
        self.step_results[step_key] = result

        # 特殊处理 cd 命令
        if command_str.strip().startswith("cd "):
            parts = command_str.strip().split(maxsplit=1)
            if len(parts) > 1:
                args = [parts[1]]
            else:
                args = []

            result.status = StepStatus.RUNNING
            success = self._handle_cd_command(args)
            result.status = StepStatus.SUCCESS if success else StepStatus.FAILED
            result.duration = time.time() - start_time
            return success

        # 特殊处理 echo 命令
        if command_str.strip().startswith("echo "):
            result.status = StepStatus.RUNNING
            parts = command_str.strip().split(maxsplit=1)
            if len(parts) > 1:
                print(f"    {parts[1]}")
            result.status = StepStatus.SUCCESS
            result.duration = time.time() - start_time
            return True

        # 解析命令
        parts = command_str.strip().split()
        if not parts:
            self._log("空命令", "ERROR", step_key)
            result.status = StepStatus.FAILED
            result.duration = time.time() - start_time
            return False

        cmd = parts[0]
        args = parts[1:] if len(parts) > 1 else []

        # 检查命令是否存在
        exists, actual_cmd = self._check_command_exists(cmd)
        if not exists:
            self._log(f"命令不存在: {cmd}", "ERROR", step_key)
            result.status = StepStatus.FAILED
            result.duration = time.time() - start_time
            return False

        try:
            result.status = StepStatus.RUNNING

            # 打印分隔线
            print(f"{'=' * 60}")
            self._log(f"执行命令: {actual_cmd} {' '.join(args)}", "INFO", step_key)

            # 执行命令 - 实时显示输出
            if self.is_windows and cmd in ["npm", "pnpm", "yarn"]:
                # Windows 上对于包管理器使用 shell=True
                full_command = f"{actual_cmd} {' '.join(args)}"
                process = subprocess.Popen(
                    full_command,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    stdin=subprocess.DEVNULL,
                    text=True,
                    bufsize=1,
                    universal_newlines=True,
                    cwd=os.getcwd()
                )
            else:
                # Unix-like 或其他命令
                process = subprocess.Popen(
                    [actual_cmd] + args,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    stdin=subprocess.DEVNULL,
                    text=True,
                    bufsize=1,
                    universal_newlines=True,
                    cwd=os.getcwd()
                )

            # 记录进程PID
            result.process_pid = process.pid

            if step_key == "step_3":
                # step_3: 记录为后台进程，但继续在前台显示输出
                result.is_background = True
                self.background_processes.append(process)

            # 实时读取输出并显示
            output_lines = []
            if wait_for_completion:
                # 阻塞模式：等待进程结束
                while True:
                    line = process.stdout.readline()
                    if not line and process.poll() is not None:
                        break
                    if line:
                        line = line.rstrip('\n')
                        output_lines.append(line)
                        print(f"    {line}")

                # 等待进程结束
                returncode = process.wait()
                result.returncode = returncode
            else:
                # 非阻塞模式：启动后立即返回
                # 先读取一些初始输出
                for _ in range(5):  # 读取前5行输出
                    try:
                        line = process.stdout.readline()
                        if line:
                            line = line.rstrip('\n')
                            output_lines.append(line)
                            print(f"    {line}")
                    except:
                        break

                # 检查进程是否仍在运行
                time.sleep(1)
                if process.poll() is None:
                    # 进程仍在运行，启动后台线程继续读取输出
                    self._log("进程启动成功，继续在后台运行...", "INFO", step_key)

                    def read_output_continuously():
                        while process.poll() is None:
                            try:
                                line = process.stdout.readline()
                                if line:
                                    line = line.rstrip('\n')
                                    print(f"    {line}")
                            except:
                                break

                    output_thread = threading.Thread(target=read_output_continuously, daemon=True)
                    output_thread.start()
                    returncode = None
                else:
                    # 进程已退出
                    returncode = process.wait()
                    result.returncode = returncode

            print(f"{'=' * 60}")

            # 记录结果
            result.stdout = "\n".join(output_lines)
            result.duration = time.time() - start_time

            if returncode is None or returncode == 0:
                if step_key == "step_3" and returncode is None:
                    # step_3 在后台运行，不检查返回码
                    self._log(f"✅ 开发服务器已启动 (PID: {process.pid})", "SUCCESS", step_key)
                    return True
                else:
                    result.status = StepStatus.SUCCESS
                    self._log(f"✅ 执行成功 (耗时: {result.duration:.2f}s)", "SUCCESS", step_key)
                    return True
            else:
                result.status = StepStatus.FAILED
                self._log(f"❌ 执行失败，退出码: {returncode} (耗时: {result.duration:.2f}s)", "ERROR", step_key)
                return False

        except Exception as e:
            result.status = StepStatus.FAILED
            result.duration = time.time() - start_time
            self._log(f"执行时发生错误: {str(e)}", "ERROR", step_key)
            import traceback
            self._log(f"详细错误: {traceback.format_exc()}", "ERROR", step_key)
            return False

    def _health_check_step_3(self, result: StepResult) -> bool:
        """对 step_3 进行健康检查"""
        if "step_3" not in self.config.health_checks:
            return True

        health_config = self.config.health_checks["step_3"]
        url = health_config.get("url", "http://localhost:5175/")
        max_attempts = health_config.get("max_attempts", 20)
        interval_seconds = health_config.get("interval_seconds", 2)
        description = health_config.get("description", "检查前端开发服务器是否就绪")

        self._log(f"🔍 开始健康检查: {description}", "HEALTH", "step_3")
        self._log(f"检查地址: {url}", "INFO", "step_3")
        self._log(f"最大尝试次数: {max_attempts}, 间隔: {interval_seconds}秒", "INFO", "step_3")

        result.status = StepStatus.HEALTH_CHECKING

        for attempt in range(1, max_attempts + 1):
            self._log(f"尝试连接 ({attempt}/{max_attempts})...", "INFO", "step_3")

            try:
                # 使用 requests.get 检查服务是否可用
                response = requests.get(url, timeout=5)

                if 200 <= response.status_code < 500:
                    self._log(f"✅ 健康检查通过! 状态码: {response.status_code}", "SUCCESS", "step_3")
                    result.health_check_passed = True
                    result.status = StepStatus.SUCCESS
                    return True
                else:
                    self._log(f"⚠️  服务返回状态码: {response.status_code}", "WARNING", "step_3")

            except requests.exceptions.Timeout:
                self._log("请求超时 (5秒)", "WARNING", "step_3")
            except requests.exceptions.ConnectionError:
                self._log("连接被拒绝，服务可能还在启动中...", "INFO", "step_3")
            except Exception as e:
                self._log(f"请求错误: {str(e)}", "WARNING", "step_3")

            # 等待下次尝试
            if attempt < max_attempts:
                time.sleep(interval_seconds)

        self._log(f"❌ 健康检查失败: 服务在 {max_attempts} 次尝试后仍不可用", "ERROR", "step_3")
        result.status = StepStatus.FAILED
        return False

    def _print_summary(self):
        """打印执行摘要"""
        print("\n" + "=" * 60)
        print("🏁 执行摘要")
        print("=" * 60)

        total_steps = len(self.step_results)
        successful = sum(1 for r in self.step_results.values() if r.status == StepStatus.SUCCESS)
        failed = sum(1 for r in self.step_results.values() if r.status == StepStatus.FAILED)
        skipped = sum(1 for r in self.step_results.values() if r.status == StepStatus.SKIPPED)
        background = sum(1 for r in self.step_results.values() if r.is_background)
        health_checked = sum(1 for r in self.step_results.values() if r.health_check_passed)

        status_icons = {
            StepStatus.SUCCESS: "✅",
            StepStatus.FAILED: "❌",
            StepStatus.SKIPPED: "⏭️",
            StepStatus.HEALTH_CHECKING: "🔍",
            StepStatus.RUNNING: "🔄",
            StepStatus.PENDING: "⏳"
        }

        for step_key, result in self.step_results.items():
            icon = status_icons.get(result.status, "❓")
            status_text = result.status.value

            if result.health_check_passed:
                status_text += " ✓"
            if result.is_background:
                status_text += " 🔄"

            print(f"{icon} {step_key}: {status_text} "
                  f"(耗时: {result.duration:.2f}s)")

            if result.process_pid:
                print(f"   └─ PID: {result.process_pid}")
            if result.skipped_reason:
                print(f"   └─ 跳过原因: {result.skipped_reason}")

        print("-" * 60)
        print(f"总计步骤: {total_steps} | "
              f"成功: {successful} | "
              f"失败: {failed} | "
              f"跳过: {skipped} | "
              f"后台进程: {background} | "
              f"健康检查: {health_checked}")

        if self.background_processes:
            print("\n🔄 仍在运行的后台进程:")
            for proc in self.background_processes:
                if proc.poll() is None:
                    print(f"   • PID {proc.pid}")

        print("=" * 60)
        if self.background_processes:
            print("💡 提示: 按 Ctrl+C 停止所有后台进程")

    def run_all_steps(self):
        """执行所有配置的步骤"""
        self._log(f"检测到操作系统: {platform.system()} {platform.release()}", "INFO")
        self._log(f"工作目录: {self.original_cwd}", "INFO")
        self._log(f"超时设置: {self.timeout} 秒", "INFO")
        self._log("开始执行配置步骤...", "INFO")

        # 按顺序执行步骤
        for step_key, command_str in self.config.steps.items():
            self._log(f"\n步骤 {step_key}", "INFO")

            if step_key == "step_3":
                # step_3: 首先检查服务是否已经在运行
                self._log("检查服务是否已在运行...", "INFO", step_key)

                # 获取健康检查的URL
                health_url = "http://localhost:5175/"
                if "step_3" in self.config.health_checks:
                    health_config = self.config.health_checks["step_3"]
                    health_url = health_config.get("url", health_url)

                # 检查服务是否已经在运行
                if self._check_service_already_running(health_url):
                    # 服务已在运行，跳过 step_3
                    result = StepResult(
                        step_name=step_key,
                        status=StepStatus.SKIPPED,
                        duration=0.0,
                        skipped_reason=f"服务已在运行: {health_url}"
                    )
                    self.step_results[step_key] = result
                    self._log(f"⏭️  跳过 {step_key}: 服务已在运行", "SKIP", step_key)
                    continue  # 跳过 step_3，继续执行后续步骤

                # 服务未运行，执行 step_3（前台显示输出，但不等待完成）
                self._log("启动开发服务器...", "INFO", step_key)
                success = self._run_foreground_step(step_key, command_str, wait_for_completion=False)

                if success:
                    # 进行健康检查
                    result = self.step_results[step_key]
                    health_success = self._health_check_step_3(result)

                    if not health_success:
                        self._log(f"\n❌ 步骤 {step_key} 健康检查失败，流程终止", "ERROR")
                        self._cleanup_background_processes()
                        self._print_summary()
                        return False
                else:
                    # step_3 启动失败
                    self._log(f"\n❌ 步骤 {step_key} 执行失败，流程终止", "ERROR")
                    self._cleanup_background_processes()
                    self._print_summary()
                    return False
            else:
                # 其他步骤: 阻塞执行，原样显示输出
                success = self._run_foreground_step(step_key, command_str, wait_for_completion=True)

            if not success:
                self._log(f"\n❌ 步骤 {step_key} 执行失败，流程终止", "ERROR")
                self._cleanup_background_processes()
                self._print_summary()
                return False

        self._log("\n✅ 所有步骤执行完成！", "SUCCESS")
        self._print_summary()
        return True

    def run(self):
        """主运行方法"""
        try:
            # 检查Python版本
            if sys.version_info < (3, 7):
                self._log("需要 Python 3.7 或更高版本", "ERROR")
                sys.exit(1)

            # 检查requests是否安装
            try:
                import requests
            except ImportError:
                self._log("正在安装 requests...", "INFO")
                try:
                    subprocess.run(
                        [sys.executable, "-m", "pip", "install", "requests"],
                        check=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True
                    )
                    self._log("✅ requests 安装成功", "SUCCESS")
                except subprocess.CalledProcessError as e:
                    self._log(f"安装 requests 失败: {e.stderr if e.stderr else str(e)}", "ERROR")
                    sys.exit(1)

            # 运行所有步骤
            success = self.run_all_steps()

            # 恢复原始工作目录
            os.chdir(self.original_cwd)

            if not success:
                self._cleanup_background_processes()
                sys.exit(1)

            # 如果有后台进程运行（step_3），等待用户中断
            if self.background_processes:
                print("\n🎯 开发环境已启动！按 Ctrl+C 停止所有服务")
                try:
                    # 监控进程输出
                    def monitor_processes():
                        while True:
                            all_stopped = True
                            for proc in self.background_processes:
                                if proc.poll() is None:
                                    all_stopped = False
                                    # 非阻塞读取输出
                                    try:
                                        if select.select([proc.stdout], [], [], 0.1)[0]:
                                            line = proc.stdout.readline()
                                            if line:
                                                print(f"[DEV SERVER] {line.rstrip()}")
                                    except:
                                        pass

                            if all_stopped:
                                break
                            time.sleep(1)

                    monitor_thread = threading.Thread(target=monitor_processes, daemon=True)
                    monitor_thread.start()

                    # 等待键盘中断或所有进程结束
                    try:
                        monitor_thread.join()
                    except KeyboardInterrupt:
                        print("\n👋 正在停止所有服务...")
                    finally:
                        self._cleanup_background_processes()
                        print("✅ 所有服务已停止")

                except KeyboardInterrupt:
                    print("\n👋 正在停止所有服务...")
                    self._cleanup_background_processes()
                    print("✅ 所有服务已停止")
                except Exception as e:
                    self._log(f"监控进程时出错: {str(e)}", "ERROR")

            self._cleanup_background_processes()

        except KeyboardInterrupt:
            self._log("\n⚠️  用户中断执行", "WARNING")
            self._cleanup_background_processes()
            sys.exit(130)
        except Exception as e:
            self._log(f"未处理的错误: {str(e)}", "ERROR")
            import traceback
            self._log(f"详细错误: {traceback.format_exc()}", "ERROR")
            self._cleanup_background_processes()
            sys.exit(1)


def run_task_cmd(config_json):
    """任务入口函数"""
    # 清理 dist 文件夹
    folder_path = "./dist"
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
        print(f"✅ 文件夹 '{folder_path}' 已删除")
    else:
        print(f"⚠️ 文件夹 '{folder_path}' 不存在")

    print("🚀 跨平台开发构建工具 v3.2")
    print("=" * 40)
    print("特性:")
    print("  • 执行 step_3 前检查服务是否已启动")
    print("  • 如果服务已在运行，跳过 step_3")
    print("  • step_3: 前台显示执行过程 + 后台健康检查")
    print("  • 其他步骤: 阻塞执行，原样显示输出")
    print("=" * 40)

    # 检查配置文件
    config_file = config_json
    if not os.path.exists(config_file):
        print(f"❌ 找不到配置文件: {config_file}")
        print("请确保配置文件存在于当前目录")
        sys.exit(1)

    # 运行构建器
    runner = CrossPlatformDevRunner(config_file)
    runner.run()


# 必要的环境检测
def check_sys_state():
    # 环境检测
    encoding = sys.getdefaultencoding()
    if encoding.lower() != "utf-8":
        print(f"你的操作系统系统默认编码不是 UTF-8 ", encoding)
        return False
    else:
        return True


# 开发环境已经运行程序
# 按dev.json步骤执行，除了“step_3”标号步骤，其它步骤会阻塞。
if __name__ == "__main__":



    if check_sys_state():
        # 直接运行
        if len(sys.argv) > 1:
            config_file = sys.argv[1]
        else:
            config_file = "dev.json"
        #
        run_task_cmd(config_file)
        pass
    else:
        print(f"系统检测不通过！")
        pass

    pass