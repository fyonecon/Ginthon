// 自定义的前端配置文件
const config = {
    debug: false, // true、false
    app: {
        app_name: "Ginthon",
        app_class: "ginthon_sv_", // ginthon_sv_ 、waigo_sv_
        app_version: "1.6.5", // 1.0.0
    },
    sys:{
        backend: "py", // go、py
        base_route: "/view", // 此值请同样svelte.config.js中paths的base：""、"/view"、'/view_static'，结尾无/
        home_route: "/home", // 主页默认页的路由：空""、"/purehome"
        home_route_white_word: "@home", // 默认刷新时打开的页面，与search里面“@白名单”匹配：空"@"、"@purehome"
    },
    api: {
        js_call_py_url: "https://127.0.0.1:9750/api/js_call_py", // http(s)://127.0.0.1:9750/api/js_call_py 、http(s)://127.0.0.1:9850/api/js_call_go
        api_host: "https://127.0.0.1:9750", // http(s)://127.0.0.1:9750、http(s)://127.0.0.1:9850
    },
};
export default config;