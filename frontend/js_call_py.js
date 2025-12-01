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

    // ==============================================================
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


    // 隐藏窗口
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


    // ==============================================================
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
console.log("js_call_py.js已加载。");
//js_call_py("test", {"a": "-a-"}).then(
//    back_data=>{
//        console.log("js_call_py返回值：", back_data);
//    }
//);
// 展示窗口
js_call_py("window_show", {}).then(
    back_data=>{
        console.log("js_call_py.js调用window_js_call_py.py返回值：", "window_show", back_data);
    }
);