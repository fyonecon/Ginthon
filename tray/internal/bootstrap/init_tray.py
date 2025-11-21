import threading
import rumps
import webview
import time


# --- pywebview 相关的逻辑（运行在主线程）---

def run_webview_app():
    """
    启动 pywebview 窗口。
    webview.start() 会阻塞主线程。
    """
    webview.create_window('PyWebView App', 'https://www.bing.com')
    # 阻塞主线程运行 GUI 循环
    webview.start()
    print("PyWebView closed.")


# --- Rumps 相关的逻辑（尝试运行在子线程）---

class AwesomeStatusBarApp(rumps.App):
    def __init__(self):
        super(AwesomeStatusBarApp, self).__init__("MyApp", menu=['Open Webview', 'Say Hi'])
        # 在 Rumps 中启动一个定时器，用于测试后台活动
        self.timer = rumps.Timer(self.tick, 5)  # 每5秒执行一次
        self.timer.start()

    @rumps.clicked("Open Webview")
    def open_webview(self, sender):
        """
        这个点击事件处理器可以在 Rumps 的线程中调用 webview 的函数。
        """
        # ⚠️ 注意：直接在非主线程中创建/操作 pywebview 窗口可能会引发问题！
        # 如果 pywebview 已经在主线程中启动并运行，则需要使用线程安全的方式与其通信。
        print("Rumps clicked 'Open Webview'. If pywebview is active, this may be fine.")
        # 如果 pywebview 尚未启动，这里调用可能会失败或启动一个新的 GUI 循环。
        # 最好只在主线程中调用 webview.create_window / webview.start
        # 并且只在启动后通过 webview.windows[0].evaluate_js 等方式进行交互。

    @rumps.clicked("Say Hi")
    def say_hi(self, sender):
        rumps.alert("Hello!")

    def tick(self, sender):
        print(f"Rumps timer ticked at {time.ctime()}")


def run_rumps_app():
    """
    启动 rumps 应用。
    rumps.run() 会启动事件循环并阻塞其所在线程。
    """
    try:
        AwesomeStatusBarApp().run()
    except Exception as e:
        # 如果 rumps 不允许在子线程运行，可能会在这里捕获错误
        print(f"Rumps Error in Thread: {e}")


# --- 主程序入口 ---

if __name__ == '__main__':
    # 1. 启动 Rumps 在一个单独的线程中
    rumps_thread = threading.Thread(target=run_rumps_app, daemon=True)
    rumps_thread.start()

    # 2. 在主线程中启动 PyWebView
    # PyWebView 的事件循环将接管主线程
    print("Starting PyWebView in main thread...")
    # run_webview_app() # <-- 解开此行注释来运行 PyWebView

    # ⚠️ 警告：
    # 如前所述，rumps 和 pywebview 通常都需要主线程。
    # 上述示例将 rumps 放在子线程中，在 macOS 上几乎肯定会失败或行为不稳定。

    # --- 替代方案：检查是否有集成点 ---
    # 如果两个库都没有提供“非阻塞”模式或事件循环集成（如与 asyncio/uvloop/其他 GUI 库集成），
    # 那么在同一进程中运行它们的唯一安全方法是使用 Process，而不是 Thread。

    print("\n--- 启动失败提示 ---")
    print("注意：rumps（在 macOS 上）和 pywebview (跨平台 GUI) 都强烈要求在主线程中运行其 GUI/事件循环。")
    print("将其中一个放在子线程中很可能导致应用崩溃或不稳定。")
    print("要解决这个问题，你通常需要：")
    print("1. 寻找两个库是否支持同一个底层 GUI 框架的事件循环集成点（例如：PyQt/wxPython/asyncio）。")
    print("2. 使用 **多进程（multiprocessing）**，而不是多线程，将它们完全隔离。")