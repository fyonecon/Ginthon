#!/usr/bin/env python3
"""
跨平台开发构建脚本
根据 build.json 配置执行步骤
支持 Windows、macOS、Linux
"""

# -*- coding: utf-8 -*-

import asyncio
import json
import sys
import os
import platform
import subprocess
import shutil
import signal
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum

from anyio import sleep


class StepStatus(Enum):
    """步骤状态枚举"""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class StepResult:
    """步骤执行结果"""
    step_name: str
    status: StepStatus = StepStatus.PENDING
    returncode: Optional[int] = None
    stdout: str = ""
    stderr: str = ""
    duration: float = 0.0


@dataclass
class Config:
    """配置文件"""
    steps: Dict[str, str] = field(default_factory=dict)
    custom_commands: Dict[str, str] = field(default_factory=dict)
    timeout_seconds: int = 120

    @classmethod
    def from_file(cls, filepath: str = "dev.json") -> "Config":
        """从文件加载配置"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # 验证必需字段
            if "steps" not in data:
                raise ValueError("配置文件中缺少 'steps' 字段")

            return cls(
                steps=data["steps"],
                custom_commands=data.get("custom_commands", {}),
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
        print(f"\n⚠️  收到信号 {signum}，正在清理...")
        sys.exit(1)

    def _init_command_map(self) -> Dict[str, str]:
        """初始化命令映射表"""
        # 默认命令
        default_commands = {
            "npm": "npm.cmd" if self.is_windows else "npm",
            "python": "python" if self.is_windows else "python3",
            "pip": "pip" if self.is_windows else "pip3",
            "cd": "cd",  # cd是shell内置命令
            "pnpm": "pnpm.cmd" if self.is_windows else "pnpm",
            "yarn": "yarn.cmd" if self.is_windows else "yarn",
            "node": "node.exe" if self.is_windows else "node",
        }

        # 用自定义命令覆盖默认值
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
            "END": "\033[0m"
        }

        # 检查是否支持颜色
        supports_color = (
                not self.is_windows or
                os.environ.get('TERM_PROGRAM') == 'vscode' or
                os.environ.get('WT_SESSION')  # Windows Terminal
        )

        if supports_color and level in colors:
            prefix = f"{colors[level]}[{level}]{colors['END']}"
        else:
            prefix = f"[{level}]"

        if step:
            prefix = f"{prefix} [{step}]"

        print(f"{prefix} {message}")

    def _check_command_exists(self, command: str) -> tuple[bool, str]:
        """检查命令是否存在，返回(是否存在, 实际命令)"""
        # 如果是cd命令，总是存在（shell内置）
        if command == "cd":
            return True, "cd"

        # 从映射表中获取命令
        cmd = self.command_map.get(command, command)

        # 尝试查找命令
        if shutil.which(cmd) is not None:
            return True, cmd

        # 尝试去掉后缀
        if self.is_windows:
            cmd_without_ext = cmd.replace('.cmd', '').replace('.exe', '')
            if shutil.which(cmd_without_ext) is not None:
                return True, cmd_without_ext

        return False, cmd

    def _parse_command(self, command_str: str) -> tuple[str, List[str]]:
        """解析命令字符串为(命令, 参数列表)"""
        parts = command_str.strip().split()
        if not parts:
            return "", []

        cmd = parts[0]
        args = parts[1:] if len(parts) > 1 else []

        return cmd, args

    def _should_use_shell(self, cmd: str, command_str: str) -> bool:
        """判断是否需要使用 shell"""
        # 总是对某些命令使用 shell
        if cmd in ["cd", "npm", "pnpm", "yarn", "pip", "python"]:
            return True

        # 如果命令中包含管道、重定向、环境变量等shell特性
        shell_special_chars = ['|', '>', '<', '&', ';', '$', '(', ')', '*', '?', '[', ']']
        for char in shell_special_chars:
            if char in command_str:
                return True

        # Windows 上对更多命令使用 shell
        if self.is_windows and cmd in ["node", "git"]:
            return True

        return False

    def _handle_cd_command(self, args: List[str]) -> bool:
        """处理cd命令"""
        if not args:
            self._log("cd 命令需要参数", "ERROR")
            return False

        target_dir = args[0]

        # 处理相对路径
        if not os.path.isabs(target_dir):
            target_dir = os.path.join(os.getcwd(), target_dir)

        # 规范化路径
        target_dir = os.path.normpath(target_dir)

        try:
            os.chdir(target_dir)
            self._log(f"切换到目录: {target_dir}", "SUCCESS")
            return True
        except FileNotFoundError:
            self._log(f"目录不存在: {target_dir}", "ERROR")
            return False
        except Exception as e:
            self._log(f"切换目录失败: {str(e)}", "ERROR")
            return False

    async def _run_single_step(self, step_key: str, command_str: str) -> bool:
        """执行单个步骤"""
        self._log(f"开始执行: {command_str}", "STEP", step_key)

        start_time = asyncio.get_event_loop().time()
        result = StepResult(step_name=step_key)
        self.step_results[step_key] = result

        # 解析命令
        cmd, args = self._parse_command(command_str)

        if not cmd:
            self._log("空命令", "ERROR", step_key)
            result.status = StepStatus.FAILED
            return False

        # 特殊处理cd命令
        if cmd == "cd":
            result.status = StepStatus.RUNNING
            success = self._handle_cd_command(args)
            result.status = StepStatus.SUCCESS if success else StepStatus.FAILED
            result.duration = asyncio.get_event_loop().time() - start_time
            return success

        # 检查命令是否存在
        exists, actual_cmd = self._check_command_exists(cmd)
        if not exists:
            self._log(f"命令不存在: {cmd}", "ERROR", step_key)
            result.status = StepStatus.FAILED
            return False

        try:
            result.status = StepStatus.RUNNING

            # 判断是否需要使用 shell
            use_shell = self._should_use_shell(cmd, command_str)

            if use_shell:
                # 使用 shell 执行完整命令
                self._log(f"使用 shell 执行命令", "INFO", step_key)
                process = await asyncio.create_subprocess_shell(
                    command_str,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    shell=True
                )
            else:
                # 对于其他命令，直接执行
                self._log(f"直接执行命令: {actual_cmd}", "INFO", step_key)
                process = await asyncio.create_subprocess_exec(
                    actual_cmd,
                    *args,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )

            # 收集输出
            stdout_data = []
            stderr_data = []

            # 修复编码问题的读取函数
            async def read_stream(stream, output_list, is_stderr=False):
                while True:
                    line = await stream.readline()
                    if not line:
                        break
                    try:
                        # 尝试 UTF-8 解码
                        text = line.decode('utf-8').rstrip()
                    except UnicodeDecodeError:
                        # 如果失败，尝试 GBK（Windows 默认）
                        try:
                            text = line.decode('gbk').rstrip()
                        except UnicodeDecodeError:
                            # 都不行，用替换模式
                            text = line.decode('utf-8', errors='replace').rstrip()

                    output_list.append(text)
                    # 实时显示输出
                    if text:
                        # 错误输出用不同前缀
                        prefix = "    [ERR]" if is_stderr else "    "
                        print(f"{prefix}{text}")

            # 并行读取stdout和stderr
            await asyncio.wait_for(
                asyncio.gather(
                    read_stream(process.stdout, stdout_data, False),
                    read_stream(process.stderr, stderr_data, True)
                ),
                timeout=self.timeout
            )

            # 等待进程完成
            returncode = await process.wait()

            # 记录结果
            result.returncode = returncode
            result.stdout = "\n".join(stdout_data)
            result.stderr = "\n".join(stderr_data)
            result.duration = asyncio.get_event_loop().time() - start_time

            if returncode == 0:
                result.status = StepStatus.SUCCESS
                self._log(f"执行成功 (耗时: {result.duration:.2f}s)", "SUCCESS", step_key)
                return True
            else:
                result.status = StepStatus.FAILED
                self._log(f"执行失败 (退出码: {returncode}, 耗时: {result.duration:.2f}s)", "ERROR", step_key)
                if result.stderr:
                    self._log(f"错误输出: {result.stderr[:200]}...", "ERROR", step_key)
                return False

        except asyncio.TimeoutError:
            result.status = StepStatus.FAILED
            result.duration = self.timeout
            self._log(f"执行超时 (超过 {self.timeout} 秒)", "ERROR", step_key)
            return False
        except FileNotFoundError:
            result.status = StepStatus.FAILED
            result.duration = asyncio.get_event_loop().time() - start_time
            self._log(f"命令未找到: {cmd}", "ERROR", step_key)
            return False
        except Exception as e:
            result.status = StepStatus.FAILED
            result.duration = asyncio.get_event_loop().time() - start_time
            self._log(f"执行错误: {str(e)}", "ERROR", step_key)
            return False

    def _print_summary(self):
        """打印执行摘要"""
        print("\n" + "=" * 60)
        print("🏁 执行摘要")
        print("=" * 60)

        total_steps = len(self.step_results)
        successful = sum(1 for r in self.step_results.values() if r.status == StepStatus.SUCCESS)
        failed = sum(1 for r in self.step_results.values() if r.status == StepStatus.FAILED)

        # 状态颜色映射
        status_colors = {
            StepStatus.SUCCESS: "✅",
            StepStatus.FAILED: "❌",
            StepStatus.SKIPPED: "⏭️",
            StepStatus.PENDING: "⏳",
            StepStatus.RUNNING: "🔄"
        }

        for step_key, result in self.step_results.items():
            status_icon = status_colors.get(result.status, "❓")
            print(f"{status_icon} {step_key}: {result.status.value} "
                  f"(耗时: {result.duration:.2f}s)")

        print("-" * 60)
        print(f"总计: {total_steps} 个步骤 | "
              f"成功: {successful} | "
              f"失败: {failed}")
        print("=" * 60)

    async def run_all_steps(self):
        """执行所有配置的步骤"""
        self._log(f"检测到操作系统: {platform.system()} {platform.release()}", "INFO")
        self._log(f"工作目录: {self.original_cwd}", "INFO")
        self._log(f"超时设置: {self.timeout} 秒", "INFO")
        self._log("开始执行配置步骤...", "INFO")

        # 按顺序执行步骤
        for step_key, command_str in self.config.steps.items():
            self._log(f"\n步骤 {step_key}", "INFO")
            print("-" * 40)

            success = await self._run_single_step(step_key, command_str)

            if not success:
                self._log(f"\n❌ 步骤 {step_key} 执行失败，流程终止", "ERROR")
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

            # 运行异步主循环
            success = asyncio.run(self.run_all_steps())

            # 恢复原始工作目录
            os.chdir(self.original_cwd)

            if not success:
                sys.exit(1)

        except KeyboardInterrupt:
            self._log("\n⚠️  用户中断执行", "WARNING")
            sys.exit(130)
        except Exception as e:
            self._log(f"未处理的错误: {str(e)}", "ERROR")
            sys.exit(1)


# 任务入口
def run_task_cmd(config_json):
    folder_path = "./dist"  # 要删除的文件夹路径
    # 确保文件夹存在
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)  # 删除文件夹及其所有内容
        print(f"✅ 文件夹 '{folder_path}' 已删除")
    else:
        print(f"⚠️ 文件夹 '{folder_path}' 不存在")
        pass
    #
    print("🚀 跨平台开发构建工具")
    print("=" * 40)

    # 检查配置文件
    config_file = config_json  # json配置文件
    if not os.path.exists(config_file):
        print(f"❌ 找不到配置文件: {config_file}")
        print("请确保 dev.json 文件存在于当前目录")
        sys.exit(1)

    # 运行构建器
    runner = CrossPlatformDevRunner(config_file)
    runner.run()
    pass


# 生成应用安装包
# 按build.json步骤执行，会阻塞。
if __name__ == "__main__":
    #
    run_task_cmd("build.json")
    pass