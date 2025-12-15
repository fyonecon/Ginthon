// 自定义的前端配置文件
const config = {
    debug: true, // true、false
    app: {
        app_class: "ginthon_sv_", // ginthon_sv_ 、waigo_sv_
        app_version: "1.4.0", // 1.0.0
    },
    sys:{
        backend: "py", // go、py
    },
    api: {
        js_call_py_url: "http://127.0.0.1:9750/", // http://127.0.0.1:9750/ 、http://127.0.0.1:9850/
    },
};
export default config;