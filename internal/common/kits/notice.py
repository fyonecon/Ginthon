
from internal.common.func import func
from internal.common.kits.main_dirpath import main_dirpath
from internal.config import get_config


import time

class notice:
    # 发送系统通知
    @staticmethod
    def send(title, msg, data_dict=None):
        if data_dict is None:
            data_dict = {
                "group": get_config("app", "app_class"),  # 分组或ID
                "icon": main_dirpath.virtual_dirpath("frontend") + "/icon.png",  # 图标 .png、.ico
                "open_url": "",  # 要打开的网址
                "app_path": "",  # 要打开的app的绝对地址
                "timeout_s": "5",  # 通知显示的时间, s
            }
            pass
        #
        plt = func.get_platform()
        func.print_log("send_notice=2=", title, msg, data_dict, plt)
        #
        if plt == "mac":
            from pync import Notifier
            #
            group = data_dict["group"]
            icon = data_dict["icon"]
            open_url = data_dict["open_url"]  # href
            open_app = "open " + data_dict["app_path"]  # "open /Applications/Ginthon.app"
            timeout = int(data_dict["timeout_s"])
            #
            if timeout is None or timeout < 2:
                timeout = 5
                pass
            #
            if len(open_url) >= 9:  # 打开链接优先于运行cmd
                open_app = ""
                pass
            else:
                open_url = ""
                pass
            #
            Notifier.notify(msg, title=title,
                            group=group,
                            appIcon=icon,
                            sound="Blow",
                            open=open_url,
                            execute=open_app,
                            timeout=timeout  # s
                            )
            pass
        elif plt == "win":
            from winotify import Notification, audio
            #
            group = data_dict["group"]
            icon = data_dict["icon"]
            open_url = data_dict["open_url"]  # href
            open_app = data_dict["app_path"]  # f"cmd:///K start {GINTHON_PATH}" 或 f"file:///{GINTHON_PATH}"
            open_app = f"cmd:///K start {open_app}"
            timeout = int(data_dict["timeout_s"])
            #
            if timeout >= 6:
                duration = "long"
                pass
            else:  # <=5s
                duration = "short"
                pass
            #
            if len(open_url) >= 9:  # 打开链接优先于运行cmd
                open_app = ""
                pass
            else:
                open_url = open_app
                pass
            #
            toast = Notification(
                title=title,
                msg=msg,
                app_id=group,
                duration=duration,  # "short" 或 "long"
                icon=icon
            )
            toast.add_actions(
                label="",
                launch=open_url
            )
            toast.set_audio(audio.Default, loop=False)
            toast.show()
            pass
        else:  # linux
            import notify2
            #
            group = data_dict["group"]
            icon = data_dict["icon"]
            open_url = data_dict["open_url"]  # href
            open_app = "open " + data_dict["app_path"]  # "open /Applications/Ginthon.app"
            timeout = int(data_dict["timeout_s"])
            #
            if timeout is None or timeout < 2:
                timeout = 5
                pass
            #
            # if len(open_url) >= 9:  # 打开链接优先于运行cmd
            #     open_app = ""
            #     pass
            # else:
            #     open_url = ""
            #     pass
            # 初始化
            notify2.init(group)
            # 简单通知
            notification = notify2.Notification(title, msg)
            notification.show()

            # 完整参数
            notification = notify2.Notification(
                title,
                msg,
                icon  # 图标名称
            )

            # 设置超时（毫秒）
            notification.set_timeout(timeout * 1000)  # ms

            # 添加动作（需要支持的应用）
            # notification.add_action("action_key", "按钮文字", callback_function)

            # 紧急级别
            notification.set_urgency(notify2.URGENCY_NORMAL)  # 低
            # notification.set_urgency(notify2.URGENCY_CRITICAL)  # 高

            # 显示
            notification.show()
            time.sleep(2)

            pass
        pass
    #
    pass

