# -*- coding: utf-8 -*-

import threading
import webbrowser
import webview

from internal.app.window.controller.display_state import display_state
from internal.common.func import func
from internal.common.kits.local_database import local_database
from internal.common.kits.main_dirpath import main_dirpath
from internal.common.kits.notice import notice
from internal.common.kits.shell import shell
from internal.config import get_config


# py_run_js对照表
def list_js_call_py(WINDOW, key, data_dict):
    #
    CONFIG = get_config("", "")
    #
    state = 0
    msg = "（null）"
    content = {}

    func.print_log("list_js_call_py=", [key, data_dict])

    # 默认
    # data_dict={}
    if key == "test" or len(key) == 0:
        js_content = rf"""
            console.log("js_call_py-test", {key}, {data_dict});
        """
        #
        state = 1
        msg = "默认Key"
        content["result"] = WINDOW.evaluate_js(js_content)
        pass
    # ===========================================================


    # 用新窗口打开目标链接
    # data_dict={url:"", "title":"new window"}
    elif key == "open_url_with_new_window":
        if data_dict.get("url") and data_dict.get("title"):
            url = data_dict["url"]
            title = data_dict["title"]
            #
            def new_window():
                webview.create_window(
                    url=url, title=title,
                    min_size=(520, 520),
                    width=520, height=520,
                    hidden=False,
                    frameless=False,
                    text_select=True,
                    transparent=False,
                    background_color="#555555",
                )
                webview.start()
                print("独立窗口已关闭：", [title, url])
                pass
            #
            if func.is_url(url):
                # 创建线程
                t1 = threading.Thread(target=new_window)
                # 启动线程
                t1.start()
                # 等待线程结束
                t1.join()
                state = 1
                msg = "YES"
            else:
                state = 0
                msg = "url格式不正确"
        else:
            state = 0
            msg = "data_dict错误"
        pass


    # 用默认浏览器打开目标链接
    # data_dict={url:"", "target":"_blank"}
    elif key == "open_url_with_default_browser":
        if data_dict.get("url") and data_dict.get("target"):
            url = data_dict["url"]
            target = data_dict["target"]
            if func.is_url(url):
                if target == "_self":
                    webbrowser.open_new_tab(url)
                elif target == "_blank":
                    webbrowser.open_new(url)
                else:
                    webbrowser.open(url)
                state = 1
                msg = "YES"
            else:
                state = 0
                msg = "url格式不正确"
        else:
            state = 0
            msg = "data_dict错误"
        pass

    # 用原始窗口打开新链接
    # data_dict={url:""}
    elif key == "open_url_with_master_window":
        if data_dict.get("url"):
            url = data_dict["url"]
            if func.is_url(url):
                WINDOW.load_url(url)
                state = 1
                msg = "YES"
            else:
                state = 0
                msg = "url格式不正确"
        else:
            state = 0
            msg = "data_dict错误"
        pass

    # js监听当前窗口是隐藏还是展示
    # data_dict={display:"showing hiding"}
    elif key == "window_display":
        if data_dict.get("display"):
            display = data_dict["display"]
            if display == "hiding":
                state = 1
                msg = display_state.set("hiding")
            elif display == "showing":
                state = 1
                msg = display_state.set("showing")
            else :
                state = 0
                msg = "url格式不正确"
        else:
            state = 0
            msg = "data_dict错误"
        pass

    # js监听当前窗口的主题
    # data_dict={theme:"dark light"}
    elif key == "window_theme":
        if data_dict.get("theme"):
            theme = data_dict["theme"]
            if theme == "dark":
                state = 1
                msg = "dark"
            elif theme == "light":
                state = 1
                msg = "light"
            else:
                state = 0
                msg = "url格式不正确"
        else:
            state = 0
            msg = "data_dict错误"
        pass

    # 设置视窗title
    # data_dict={title:""}
    elif key == "window_title":
        if data_dict.get("title"):
            title = data_dict["title"]
            if len(title)==0:
                title = CONFIG["app"]["app_name"]
                pass
            elif len(title) >= 8:
                title = title[:8]+".."
                pass
            try: # 做兼容处理
                WINDOW.set_title(title)
            except:
                try:
                    WINDOW.title(title)
                except:
                    print("不支持此方法：", key)
                    pass
                pass
        else:
            state = 0
            msg = "data_dict错误"
        pass

    # 隐藏窗口
    # data_dict={}
    elif key == "window_hide":
        WINDOW.hide()
        display = display_state.set("hiding")
        #
        state = 1
        msg = "OK"
        content["display"] = display
        pass

    # 显示窗口
    # data_dict={}
    elif key == "window_show":
        WINDOW.show()
        # WINDOW.focus()
        display = display_state.set("showing")
        #
        state = 1
        msg = "OK"
        content["display"] = display
        pass

    # 改变窗口大小
    # data_dict={size_tag: "", width: 0, height: 0}
    elif key == "change_window_size":
        # 同init_window参数
        init_width = 960
        init_height = 700
        # 获取屏幕尺寸
        import screeninfo
        screen_width = init_width
        screen_height = init_height
        for monitor in screeninfo.get_monitors():
            if monitor.is_primary:
                screen_width = monitor.width
                screen_height = monitor.height
                #
                break
        # 设置屏幕尺寸
        size_tag = data_dict["size_tag"]
        if size_tag == "size_init": # 还原窗口
            width = init_width
            height = init_height
            WINDOW.resize(width=width, height=height)
            # 屏幕居中
            x = (screen_width - width) // 2
            y = (screen_height - height) // 2
            WINDOW.move(x, y)
        elif size_tag == "size_full_height": # 上下对齐
            width = screen_width/3*2
            height = screen_height
            if width < init_width:
                width = init_width
                pass
            WINDOW.resize(width=width, height=height)
            # 屏幕居中
            x = (screen_width - width) // 2
            y = 0
            WINDOW.move(x, y)
        elif size_tag == "size_full_window":  # 上下左右对齐
            width = screen_width
            height = screen_height
            WINDOW.resize(width=width, height=height)
            # 屏幕居中
            x = 0
            y = 0
            WINDOW.move(x, y)
        elif size_tag == "size_full_screen": # 全屏
            WINDOW.toggle_fullscreen()
        elif size_tag == "size_center":
            # 屏幕居中
            win_width = WINDOW.width
            win_height = WINDOW.height
            x = (screen_width - win_width) // 2
            y = (screen_height - win_height) // 2
            WINDOW.move(x, y)
        else:
            # 自定义尺寸
            width = int(data_dict["width"])
            height = int(data_dict["height"])
            # 校验
            if width > screen_width or width < 320:
                width = screen_width
                pass
            if height > screen_height or height < 320:
                height = screen_height
                pass
            WINDOW.resize(width=width, height=height)
            # 屏幕居中
            x = (screen_width - width) // 2
            y = (screen_height - height) // 2
            WINDOW.move(x, y)
            #
            pass
        #
        state = 1
        msg = "OK"
        content["size_tag"] = size_tag
        content["window_size"] = [WINDOW.width, WINDOW.height]
        content["screen_size"] = [screen_width, screen_height]
        pass

    # 显示系统通知
    # data_dict={}
    elif key == "send_notice":
        if data_dict is None:
            data_dict = { # 参数格式
                "title": "（？）",
                "msg": "（？？？）",
                "group": get_config("app", "app_class"),  # 分组或ID
                "icon": main_dirpath.virtual_dirpath("frontend") + "/icon.png",  # 图标 .png、.ico
                "open_url": "",  # 要打开的网址
                "app_path": "",  # 要打开的app的绝对地址
                "timeout_s": 5,  # 通知显示的时间
            }
            pass
        #
        title = data_dict["title"]
        msg = data_dict["msg"]
        notice.send(title, msg, data_dict)
        #
        state = 1
        msg = "OK"
        # content["display"] = display
        pass

    # 更新本地数据
    # data_dict={data_key:"", data_value:"", data_timeout_s:3600}
    elif key == "set_data":
        if data_dict.get("data_key") and data_dict.get("data_value") and data_dict.get("data_timeout_s"):
            _key = data_dict["data_key"]
            _value = data_dict["data_value"]
            _timeout_s = data_dict["data_timeout_s"]
            # 兼容格式
            try:
                _timeout_s = int(_timeout_s)
                pass
            except:
                pass
            #
            if _timeout_s <= 5*60: # 最短5min
                _timeout_s = 5*60
                pass
            #
            _value = local_database.set_data(_key, _value, _timeout_s)
            #
            state = 1
            msg = "OK"
            content["data"] = _value
        else:
            state = 0
            msg = "data_dict参数不全"
            content["data"] = ""
            pass
        pass

    # 读取本地数据
    # data_dict={data_key:""}
    elif key == "get_data":
        if data_dict.get("data_key"):
            _key = data_dict["data_key"]
            _value, _state = local_database.get_data(_key)
            #
            if _state == -1:
                state = 0
                msg = "Not Set"
                content["data"] = ""
            else:
                state = 1
                msg = "OK"
                content["data"] = _value
            pass
        else:
            state = 0
            msg = "data_dict参数不全"
            content["data"] = ""
            pass
        pass

    # 删除本地数据
    # data_dict={data_key:""}
    elif key == "del_data":
        if data_dict.get("data_key"):
            _key = data_dict["data_key"]
            _state = local_database.del_data(_key)
            if _state == -1:
                msg = "No File"
            else:
                msg = "Del OK"
            pass
            state = 1
        else:
            state = 0
            msg = "data_dict参数不全"
            pass
        pass

    # 删除本地数据
    # data_dict={filepath:""}
    elif key == "open_in_folder":
        if data_dict.get("filepath"):
            _filepath = data_dict["filepath"]
            if func.has_dir(_filepath) or func.has_file(_filepath):
                _state = shell.open_in_folder(_filepath)
                if _state:
                    state = 1
                    msg = "Open in folder"
                else:
                    state = 0
                    msg = "Open Failed"
                pass
            else:
                state = 0
                msg = "filepath不存在"
                pass
        else:
            state = 0
            msg = "data_dict参数不全"
            pass
        pass


    # ===========================================================
    # else
    # data_dict={}
    else:
        js_content = rf"""
            console.log("py_run_js-else");
        """
        #
        state = 0
        msg = "不白名单的Key"
        content["result"] = WINDOW.evaluate_js(js_content)
        pass

    #
    return {
        "state": state,
        "msg": msg,
        "content": content,
    }
    #