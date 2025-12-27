import func from "./common/func.svelte.js";

// wails专用（在Ginthon中无任何作用，仅限代码跨平台同步）
// import {Events} from "@wailsio/runtime";
// import {AppServicesForWindow} from "../bindings/datathink.top/Waigo/internal/bootstrap";

// 配合window底层，需要初始化runtime才能得到的参数
export function watch_window(){
//
    if (func.is_gthon()) {
        try {
            // 展示主窗口
            func.js_call_py_or_go("window_show", {}).then((back_data) => {
                func.console_log("[视窗JS-Log]", "js_call_py.py返回值：", back_data);
            });
        } catch(e) {
            console.error("不能导入gthon-UI相关文件");
        }
    } else if (func.is_wails()) {
        // try {
        //     // GoRunJS写入token，用于验证js_call_go
        //     Events.On("make_window_token", (result) => {
        //         const info = func.string_to_json(result.data);
        //         const app_class = config.app.app_class;
        //         // 设置新的
        //         const window_token = info.content["windowToken"];
        //         const js_call_go_api = info.content["jsCallGoApi"];
        //         const window_token_timer = func.get_time_s_date("YmdHis");
        //         //
        //         func.set_local_data(app_class+"window_token", window_token);
        //         func.set_local_data(app_class+"js_call_go_api", js_call_go_api);
        //         func.set_local_data(app_class+"window_token_timer", window_token_timer)
        //         //
        //         const key = "stop_go_run_js_for_make_window_token";
        //         const data_dict = {};
        //         func.js_call_py_or_go(key, data_dict).then(res=>{
        //             if (res.state === 1){ // 成功
        //                 console.log("[func.js_call_go]",res);
        //             }else{
        //                 console.log(res.msg, res)
        //             }
        //         });
        //     });
        //     //
        //     AppServicesForWindow.JSCallGo("test", {"data1": 2}).then(res=>{
        //         console.log("[AppServicesForWindow-JSCallGo]", res);
        //     })
        //     AppServicesForWindow.Test().then(res=>{
        //         console.log("[AppServicesForWindow-JSCallGo]", res);
        //     })
        // }catch (e) {
        //     console.error("不能导入Wails-UI相关文件");
        // }

    } else {
        console.warn("Runtime：", "请指明Web运行的浏览器环境，否则数据不能初始化，只能使用简易Web功能。", func.is_gthon(), func.is_wails(), func.get_agent(), func.get_href());
    }
}