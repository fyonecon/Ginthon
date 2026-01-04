
// 自定义的前端配置文件
import {csr} from "./routes/+page.js";

const config = {
    debug: false, // true、false
    app: {
        app_name: "Ginthon",
        app_class: "ginthon_sv_", // ginthon_sv_ 、waigo_sv_
        app_version: "1.6.4", // 1.0.0
    },
    sys:{
        backend: "py", // go、py
        base_route: "/view", // 等同于svelte.config.js中paths的base "", "/view"，结尾无/
        home_route: "/home", // 主页默认页的路由 ""、"/home"
    },
    api: {
        js_call_py_url: "https://127.0.0.1:9750/api/js_call_py", // http(s)://127.0.0.1:9750/api/js_call_py 、http(s)://127.0.0.1:9850/api/js_call_go
        api_host: "https://127.0.0.1:9750", // http(s)://127.0.0.1:9750、http(s)://127.0.0.1:9850
    },
};
export default config;