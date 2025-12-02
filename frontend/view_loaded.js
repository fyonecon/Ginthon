// loaded

// 监听和初始化页面
(function(){
    console.log("view_loaded.js已加载。");

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