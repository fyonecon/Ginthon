// 自定义的前端配置文件
const config = {
    debug: false, // true、false
    app: {
        app_name: "Ginthon",
        app_class: "ginthon_sv_", // ginthon_sv_ 、waigo_sv_
        app_version: "1.6.3", // 1.0.0
    },
    sys:{
        backend: "py", // go、py
        home_route: "/home" // 主页默认页的路由 “”、"/home”
    },
    api: {
        js_call_py_url: "http://127.0.0.1:9750/api/js_call_py", // http://127.0.0.1:9750/api/js_call_py 、http://127.0.0.1:9850/api/js_call_go
        api_host: "http://127.0.0.1:9750", // http://127.0.0.1:9750、http://127.0.0.1:9850
    },
};
export default config;