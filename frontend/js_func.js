//
// js远程调用py
const js_call_py_request = function (api_url, data_dict) {
    // 基础 POST 请求
   async function FetchPOST(url, data) {
        const config = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: typeof data === 'string' ? data : JSON.stringify(data),
            mode: 'cors', // cors, no-cors, same-origin
            cache: 'no-cache', // default, no-cache, reload, force-cache, only-if-cached
            timeout: 4, // 自定义超时 s
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
                        "data_dict": data_dict,
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
                return result;
            }
        } catch (error) {
            console.error('Fetch error 1:', error);
            return {
                "state": 0,
                "msg": "请求失败2",
                "content": {
                    "data_dict": data_dict,
                    "error": error,
                }
            };
        }
    }
    //
    return new Promise(resolve => {
        try {
            FetchPOST(api_url, data_dict).then(result=>{
                resolve(result);
            });
        } catch (error) {
            console.error('Fetch error 2:', error);
            resolve({
                "state": 0,
                "msg": "请求失败3",
                "content": {
                    "data_dict": data_dict,
                    "error": error,
                }
            });
        }
    });
};

// 监听并设置窗口的当前是否展示在前台
const window_display_on_watch = function (){
    // 检查当前页面是否隐藏（最小化或切换标签页）
    const isMinimized = document.hidden;
    // 或者使用 visibilityState
    const isVisible = document.visibilityState === 'visible';
    const isHidden = document.visibilityState === 'hidden';
    // 添加事件监听器
    document.addEventListener('visibilitychange', () => {
        let display = "hiding";
        if (document.hidden) {
            //console.log('页面被隐藏（最小化或切换标签）');
            display = "hiding";
        } else {
            //console.log('页面可见');
            display = "showing";
        }
        //
        try{
            js_call_py("window_display", {"display": display}).then(
                back_data=>{
                    console.log("[视窗JS-Log]", back_data["content"]["key"], "js_call_py.py返回值：", back_data["content"]["result"]);
                }
            );
        }catch(e){}

    });
};

// 监听页面的主题
//const window_theme_on_watch = function (){
//    let the_theme = window.matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light";
//    function change_theme(theme){
//        js_call_py("window_theme", {"theme": theme}).then(
//            back_data=>{
//                //console.log(back_data["content"]["key"], "js_call_py.py返回值：", back_data["content"]["result"]);
//            }
//        );
//    }
//    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
//        if (e.matches) {
//            //console.log('切换到暗黑模式');
//            the_theme = "dark";
//        } else {
//            //console.log('切换到浅色模式');
//            the_theme = "light";
//        }
//        change_theme(the_theme)
//    });
//    change_theme(the_theme);
//};

// 监听和初始化页面
(function(){
    console.log("js_func.js已加载。");

//    js_call_py("window_show", {}).then(
//        back_data=>{
//            console.log("[视窗JS-Log]", back_data["content"]["key"], "js_call_py.py返回值：", back_data["content"]);
//        }
//    );

    // 监测行为
//    window_display_on_watch();
//    window_theme_on_watch();

    // ==========test=============
    //// new窗口
    //js_call_py("open_url_with_default_browser", {
    //    "url": "http://127.0.0.1",
    //    "title": "窗口",
    //    "target": "_self"
    //}).then(
    //      back_data=>{
    //          console.log("[视窗JS-Log]", back_data["content"]["key"], "js_call_py.py返回值：", back_data["content"]["result"]);
    //      }
    //);
//     js_call_py("window_title", {"title": "主窗口"}).then(
//        back_data=>{
//            //console.log("[视窗JS-Log]", back_data["content"]["key"], "js_call_py.py返回值：", back_data["content"]["result"]);
//        }
//    );
//    js_call_py("dom_can_drag_window", {"dom_id": "h2"}).then(
//        back_data=>{
//            //console.log("[视窗JS-Log]", back_data["content"]["key"], "js_call_py.py返回值：", back_data["content"]["result"]);
//        }
//    );

    // 设置数据
//    js_call_py("get_data", {data_key:"test", data_value:"11111-111", data_timeout_s: 10*60}).then(
//        back_data=>{
//            console.log("[视窗JS-Log]", back_data["content"]["key"], "js_call_py.py返回值：", back_data["content"]["result"]);
//        }
//    );


})();