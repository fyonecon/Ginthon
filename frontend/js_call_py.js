// Page Loaded以后可以调用。
// js对照表
const js_call_py = function(key, data_dict){
    // 校验参数
    let api_url = "";
    try{
        api_url = js_call_py_api + "/" + js_call_py_auth + "?key=" + key;
        if (JSON.stringify(data_dict) === "{}"){data_dict={"KEY": key}} // 空的话就默认一个值
    }catch(e){
        return {"state": 0,"msg": "auth参数不全", "key": key, "data_dict": data_dict, "result": {}}
    }
    // 基本格式数据
    let back_data = {
        "state": 1,
        "msg": "js初次数据",
        "content": {
            "key": key,
            "data_dict": data_dict,
        }
    };

    // test
    // data_dict={}
    if (key === "test"){
        return new Promise(resolve => {
             js_call_py_request(api_url, back_data).then(result=>{ // 远程调用py
                resolve(result);
            });
        });
    }
    // ==============================================================



    // js监听当前窗口是隐藏还是展示
    // data_dict={display:"showing hiding"}
    else if(key === "window_display"){
        return new Promise(resolve => {
            js_call_py_request(api_url, back_data).then(result=>{ // 远程调用py
                resolve(result);
            });
        });
    }
    // 系统主题（亮、暗）
    // data_dict={theme:"dark light"}
    else if(key === "window_theme"){
        return new Promise(resolve => {
            js_call_py_request(api_url, back_data).then(result=>{ // 远程调用py
                resolve(result);
            });
        });
    }
    // 设置视窗title
    // data_dict={title:""}
    else if(key === "window_title"){
        return new Promise(resolve => {
            js_call_py_request(api_url, back_data).then(result=>{ // 远程调用py
                resolve(result);
            });
        });
    }
    // 隐藏窗口
    // data_dict={}
    else if(key === "window_hide"){
        return new Promise(resolve => {
            js_call_py_request(api_url, back_data).then(result=>{ // 远程调用py
                resolve(result);
            });
        });
    }
    // 显示窗口
    // data_dict={}
    else if(key === "window_show"){
        return new Promise(resolve => {
            js_call_py_request(api_url, back_data).then(result=>{ // 远程调用py
                resolve(result);
            });
        });
    }
    // 标签可拖拽窗口
    // data_dict={dom_id:""}
    else if(key === "dom_can_drag_window"){
        return new Promise(resolve => {
            try{
                dom_id = data_dict["dom_id"];
                let dom = document.getElementById(dom_id);
                state = 1;
                msg = "标签可拖拽窗口";
                dom.classList.add("pywebview-drag-region");
                dom.classList.add("dom_can_drag_window");
                dom.style.cssText = "-moz-user-select: none;-webkit-user-select: none;-ms-user-select: none;user-select: none;";
            }catch(e){
                state = 0;
                msg = "‘标签+ID’不存在";
            }
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
    // 用新窗口打开
    // data_dict={url:"", "title":"new window"}
    else if(key === "open_url_with_new_window"){
        return new Promise(resolve => {
             js_call_py_request(api_url, back_data).then(result=>{ // 远程调用py
                resolve(result);
            });
        });
    }
    // 用原始窗口打开新链接
    // data_dict={url:""}
    else if(key === "open_url_with_master_window"){
        return new Promise(resolve => {
            js_call_py_request(api_url, back_data).then(result=>{ // 远程调用py
                resolve(result);
            });
        });
    }
    // 用默认浏览器打开目标链接
    // data_dict={url:"", "target":"_blank"}
    else if(key === "open_url_with_default_browser"){
        return new Promise(resolve => {
            js_call_py_request(api_url, back_data).then(result=>{ // 远程调用py
                resolve(result);
            });
        });
    }

    // 更新本地数据
    // data_dict={data_key:"", data_value:"", data_timeout_s:3600}
    // data_timeout_s最短5min
    else if(key === "set_data"){
        return new Promise(resolve => {
            js_call_py_request(api_url, back_data).then(result=>{ // 远程调用py
                resolve(result);
            });
        });
    }
    // 读取本地数据
    // data_dict={data_key:""}
    else if(key === "get_data"){
        return new Promise(resolve => {
            js_call_py_request(api_url, back_data).then(result=>{ // 远程调用py
                resolve(result);
            });
        });
    }
    // 删除本地数据
    // data_dict={data_key:""}
    else if(key === "del_data"){
        return new Promise(resolve => {
            js_call_py_request(api_url, back_data).then(result=>{ // 远程调用py
                resolve(result);
            });
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

    // 展示主窗口
    js_call_py("window_show", {}).then(
        back_data=>{
            console.log(back_data["content"]["key"], "js_call_py.py返回值：", back_data["content"]["result"]);
        }
    );
    // 监测行为
    window_display_on_watch();
    window_theme_on_watch();

    // ==========test=============
    //// new窗口
    //js_call_py("open_url_with_default_browser", {
    //    "url": "http://127.0.0.1",
    //    "title": "窗口",
    //    "target": "_self"
    //}).then(
    //      back_data=>{
    //          console.log(back_data["content"]["key"], "js_call_py.py返回值：", back_data["content"]["result"]);
    //      }
    //);
//     js_call_py("window_title", {"title": "主窗口"}).then(
//        back_data=>{
//            //console.log(back_data["content"]["key"], "js_call_py.py返回值：", back_data["content"]["result"]);
//        }
//    );
//    js_call_py("dom_can_drag_window", {"dom_id": "h2"}).then(
//        back_data=>{
//            //console.log(back_data["content"]["key"], "js_call_py.py返回值：", back_data["content"]["result"]);
//        }
//    );

    // 设置数据
//    js_call_py("get_data", {data_key:"test", data_value:"11111-111", data_timeout_s: 10*60}).then(
//        back_data=>{
//            console.log(back_data["content"]["key"], "js_call_py.py返回值：", back_data["content"]["result"]);
//        }
//    );


})();
