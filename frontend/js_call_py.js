// Page Loaded以后可以调用。
// js对照表
const js_call_py = function(key, data_dict){
    let state = 0
    let msg = "";
    let back_data = {};
    let api_url = "";
    // 校验参数
    try{
        api_url = js_call_py_api + "/" + js_call_py_auth;
        if (JSON.stringify(data_dict) === "{}"){data_dict={"KEY": key}} // 空的话就默认一个值
    }catch(e){
        return {"state": 0,"msg": "auth参数不全", "key": key, "data_dict": data_dict, "result": {}}
    }


    // data_dict={}
    if (key === "test"){
        return new Promise(resolve => {
            state = 1;
            msg = "key默认值";
            //
            back_data = {
                "state": state,
                "msg": msg,
                "content": {
                    "key": key,
                    "data_dict": data_dict,
                }
            };
            back_data["result"] = js_call_py_request(api_url, back_data), // 远程调用py
            resolve(back_data);
        });
    }
    // ==============================================================

    // js监听当前窗口是隐藏还是展示
    // data_dict={display="showing hiding"}
    else if(key === "window_display"){
        return new Promise(resolve => {
            state = 1;
            msg = "js监听当前窗口是隐藏还是展示";
            //
            back_data = {
                "state": state,
                "msg": msg,
                "content": {
                    "key": key,
                    "data_dict": data_dict,
                }
            };
            back_data["result"] = js_call_py_request(api_url, back_data),  // 远程调用py
            resolve(back_data);
        });
    }
    // data_dict={theme="dark light"}
    else if(key === "window_theme"){
        return new Promise(resolve => {
            state = 1;
            msg = "js监听当前窗口的主题";
            //
            back_data = {
                "state": state,
                "msg": msg,
                "content": {
                    "key": key,
                    "data_dict": data_dict,
                }
            };
            back_data["result"] = js_call_py_request(api_url, back_data),  // 远程调用py
            resolve(back_data);
        });
    }
    // 隐藏窗口
    // data_dict={}
    else if(key === "window_hide"){
        return new Promise(resolve => {
            state = 1;
            msg = "隐藏窗口";
            //
            back_data = {
                "state": state,
                "msg": msg,
                "content": {
                    "key": key,
                    "data_dict": data_dict,
                }
            };
            back_data["result"] = js_call_py_request(api_url, back_data),  // 远程调用py
            resolve(back_data);
        });
    }
    // 显示窗口
    // data_dict={}
    else if(key === "window_show"){
        return new Promise(resolve => {
            state = 1;
            msg = "显示窗口";
            //
            back_data = {
                "state": state,
                "msg": msg,
                "content": {
                    "key": key,
                    "data_dict": data_dict,
                }
            };
            back_data["result"] = js_call_py_request(api_url, back_data),  // 远程调用py
            resolve(back_data);
        });
    }
    // 用新窗口打开
    // data_dict={url="", "title"="new window"}
    else if(key === "open_url_with_new_window"){
        return new Promise(resolve => {
            state = 1;
            msg = "用新窗口打开";
            //
            back_data = {
                "state": state,
                "msg": msg,
                "content": {
                    "key": key,
                    "data_dict": data_dict,
                }
            };
            back_data["result"] = js_call_py_request(api_url, back_data),  // 远程调用py
            resolve(back_data);
        });
    }
    // 用原始窗口打开新链接
    // data_dict={url=""}
    else if(key === "open_url_with_master_window"){
        return new Promise(resolve => {
            state = 1;
            msg = "用主窗口打开";
            //
            back_data = {
                "state": state,
                "msg": msg,
                "content": {
                    "key": key,
                    "data_dict": data_dict,
                }
            };
            back_data["result"] = js_call_py_request(api_url, back_data),  // 远程调用py
            resolve(back_data);
        });
    }
    // 用默认浏览器打开目标链接
    // data_dict={url="", "target"="_blank"}
    else if(key === "open_url_with_default_browser"){
        return new Promise(resolve => {
            state = 1;
            msg = "用默认浏览器打开";
            //
            back_data = {
                "state": state,
                "msg": msg,
                "content": {
                    "key": key,
                    "data_dict": data_dict,
                }
            };
            back_data["result"] = js_call_py_request(api_url, back_data),  // 远程调用py
            resolve(back_data);
        });
    }


    // ==============================================================
    // data_dict={}
    else {
        return new Promise(resolve => {
            state = 1;
            msg = "key不在白名单";
            //
            back_data = {
                "state": state,
                "msg": msg,
                "content": {
                    "key": key,
                    "data_dict": data_dict,
                    "result": {},
                }
            };
            resolve(back_data);
        });
    }
};

// 监听和初始化页面
(function(){
    console.log("js_call_py.js已加载。");
    // 展示窗口
    js_call_py("window_show", {}).then(
        back_data=>{
            console.log(back_data["content"]["key"], "js_call_py.js调用window_js_call_py.py返回值：", back_data);
        }
    );
    //// new窗口
    //js_call_py("open_url_with_default_browser", {
    //    "url": "http://127.0.0.1",
    //    "title": "窗口",
    //    "target": "_self"
    //}).then(
    //      back_data=>{
    //          console.log(back_data["content"]["key"], "js_call_py.js调用window_js_call_py.py返回值：", back_data);
    //      }
    //);
    // watch
    window_display_on_watch();
    window_theme_on_watch();
})();
