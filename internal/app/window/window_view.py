from internal.bootstrap.app_auth import make_rand_token
from internal.common.func import get_time_s, get_date
from internal.common.kits.main_dirpath import mian_virtual_dirpath
import os

from internal.config import get_config


# 视图view
def window_view(_WINDOW, rand_id, filename):
    #
    def read_html(the_file):
        content = ""
        if os.path.exists(the_file):  # 存在文件或文件夹
            if os.path.isfile(the_file):  # 是文件
                with open(the_file, "r", encoding="utf-8") as file:
                    content = file.read()
                    pass
        return content
    #
    config = get_config()
    #
    view_host = config["pywebview"]["view_host"]
    view_url = view_host+":"+str(config["flask"]["port"])+"/view"
    view_html = view_url + "/" + filename
    file_path = mian_virtual_dirpath("frontend") + "/view/"+filename
    #
    js_call_py_url = view_host+":"+str(config["flask"]["port"])+"/"+ "js_call_py.js" + "?cache=" + str(get_time_s()) + "&app_version=" + config["app"]["app_version"]
    #
    app_class = config["app"]["app_class"]
    salt_str = "js_call_py_auth-2025"
    timeout_s = 2*365*24*3600
    #
    js_call_py_auth = make_rand_token(app_class, salt_str, timeout_s, config)
    #
    js_call_py_api = view_host+":"+str(config["flask"]["port"])+"/api/js_call_py"
    #
    html = read_html(file_path)
    js_request = '''
        // js远程调用py
        const js_call_py_request = function (api_url, data_dict) {
            // 基础 POST 请求
            async function FetchPOST(url, data, options = {}) {
                const config = {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: typeof data === 'string' ? data : JSON.stringify(data),
                    mode: options.mode || 'cors', // cors, no-cors, same-origin
                    cache: options.cache || 'no-cache', // default, no-cache, reload, force-cache, only-if-cached
                };
                try {
                    const response = await fetch(url, config);
                    // 检查响应状态
                    if (!response.ok) {
                        // throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                        return {
                            "state": 0,
                            "msg": "请求失败1",
                            "content": {
                                "error status": response.status,
                                "error text": response.statusText,
                            }
                        };
                    }else{
                        // 根据 Content-Type 解析响应
                        const contentType = response.headers.get('content-type');
                        let result;
                        if (contentType && contentType.includes('application/json')) {
                            result = await response.json();
                        } else if (contentType && contentType.includes('text/')) {
                            result = await response.text();
                        } else if (contentType && contentType.includes('form-data')) {
                            result = await response.formData();
                        } else if (contentType && contentType.includes('blob')) {
                            result = await response.blob();
                        } else {
                            result = await response.text();
                        }
                        // let res =  {
                        //     status: response.status,
                        //     statusText: response.statusText,
                        //     headers: Object.fromEntries(response.headers.entries()),
                        //     data: result,
                        //     ok: response.ok,
                        //     redirected: response.redirected,
                        //     type: response.type,
                        //     url: response.url
                        // };
                        // console.log(api_url, data_dict, res);
                        return result;
                    }
                } catch (error) {
                    console.error('Fetch error:', error);
                    return {
                        "state": 0,
                        "msg": "请求失败2",
                        "content": {
                            "error": error,
                        }
                    };
                }
            }
            //
            return new Promise(resolve => {
                try {
                    const response = FetchPOST(api_url, data_dict, {
                        timeout: 6 // 自定义超时 s
                    });
                    resolve(response.data);
                } catch (error) {
                    resolve({
                        "state": 0,
                        "msg": "请求失败3",
                        "content": {
                            "error": error,
                        }
                    });
                }
            });
        };
    '''
    js_on_watch = '''
        // 监听并设置窗口的当前是否展示在前台
        function window_display_on_watch(){
            // 检查当前页面是否隐藏（最小化或切换标签页）
            const isMinimized = document.hidden;
            // 或者使用 visibilityState
            const isVisible = document.visibilityState === 'visible';
            const isHidden = document.visibilityState === 'hidden';
            // 添加事件监听器
            document.addEventListener('visibilitychange', () => {
                let display = "";
                if (document.hidden) {
                    //console.log('页面被隐藏（最小化或切换标签）');
                    display = "hiding";
                } else {
                    //console.log('页面可见');
                    display = "showing";
                }
                js_call_py("window_display", {"display": display}).then(
                    back_data=>{
                        console.log(back_data["content"]["key"], "js_call_py.js调用window_js_call_py.py返回值：", back_data);
                    }
                );
            });
        }
        // 监听页面的主题
        function window_theme_on_watch(){
            let the_theme = window.matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light";
            function change_theme(theme){
                js_call_py("window_theme", {"theme": theme}).then(
                    back_data=>{
                        console.log(back_data["content"]["key"], "js_call_py.js调用window_js_call_py.py返回值：", back_data);
                    }
                );
            }
            window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
                if (e.matches) {
                    //console.log('切换到暗黑模式');
                    the_theme = "dark";
                } else {
                    //console.log('切换到浅色模式');
                    the_theme = "light";
                }
                change_theme(the_theme)
            });
            change_theme(the_theme);
        }
    '''
    js_loaded = f'''
        <script class="window-script" id="window_must_data">
            const view_url = "{view_url}";
            const view_html = "{view_html}"; 
            const view_filename = "{filename}"; 
            const js_call_py_api = "{js_call_py_api}"; 
            const js_call_py_auth = "{js_call_py_auth}"; 
        </script>
        <script class="window-script" id="window_reqeust">{js_request}</script>
        <script class="window-script" id="window_on_watch">{js_on_watch}</script>
        <script class="window-script" id="window_js_call_py" src="{js_call_py_url}"></script>
    '''
    if len(html)==0:
        html = '''
        <html lang="zh">
        <head>
            <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0, user-scalable=0" />
            <title>Default Window</title>
            <style>
                .hide{
                    display: none !important;
                }
                .click{
                    cursor: pointer;
                }
                .click:active{
                    opacity: 0.6;
                }
                .select-none{
                    -moz-user-select: none;-webkit-user-select: none;-ms-user-select: none;
                    user-select: none;
                }
                .break{
                    overflow: hidden;
                    word-wrap: break-word;
                    overflow-wrap: break-word;
                }
            </style>
        </head>
        <body style="background-color: transparent;">
            <br/>
            <h2 style="text-align: center; " class="select-none">当前使用了空模板。</h2>
            <div style="text-align: center;">
                <p id="info" class="break"></p>
                <p class="select-none"><img src="http://127.0.0.1:9100/file/test.png" width="192" alt=""/></p>
            </div>
            <script>
            function show_info(_view_html) {
                let info = [
                    window.location.host, 
                    !!window.localStorage, 
                    !!window.indexedDB, 
                    navigator.webdriver, 
                    navigator.languages, 
                    window.matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light", "✅", 
                    window.navigator.userAgent,
                    view_url,
                    view_html,
                ]; 
                console.log(info);
                document.getElementById("info").innerHTML = view_filename+" 文件不存在。"; 
            }
            show_info(view_html);
            </script>
        </body>
        </html>
        '''
        pass

    return js_loaded+html