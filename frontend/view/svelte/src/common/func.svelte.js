import { redirect } from "@sveltejs/kit";
import { goto } from '$app/navigation';
import { page } from '$app/state';
import { browser } from '$app/environment';
import md5 from 'md5';
import config from "../config";
import lang_dict from "../common/translate";
import FetchGET from "./get.svelte";
import dexie_kv_db from "./db_kv.svelte";
import {alert_data} from "../stores/alert.store.svelte";
import {loading_data} from "../stores/loading.store.svelte";
import {notice_data} from "../stores/notice.store.svelte";
import {watch_lang_data} from "../stores/watch_lang.store.svelte";
import {app_uid_data} from "../stores/app_uid.store.svelte";
import FetchPOST from "./post.svelte";
import {input_enter_data} from "../stores/input_enter.store.svelte.js";
import QRCode from "qrcode";


//
let loading_show_timer = $state(0);
let alert_msg_timer = $state(0);
let size_tag = $state("size_init");


// 复用函数
// 调用xxx = func.test();
const func = {
    test: function(data_dict){
        let that = this;
        console.log("test=", data_dict);
    },
    console_log: function(...args){
        if (config.debug){
            console.log("[Log]", ...args);
        }else {
            //
        }
    },
    console_error: function(...args){
        if (config.debug){
            console.error("[Error]", ...args);
        }else {
            //
        }
    },
    title: function(_title="-"){
        if (browser){
            document.title = _title;
        }
    },
    url_path: function(pathname){ // URL的path路径前缀，适配后端服务器输出规则。默认""，推荐"."。pathname开头/ 。
        let new_path = config.sys.base_route+pathname;
        new_path = new_path.replaceAll("//", "/");
        return new_path;
    },
    redirect_pathname: function (data_dict){ // 重定向到新路由。相当于301永久重定向。 url_pathname开头/
        let that = this;
        //
        const url_pathname = data_dict['url_pathname'];
        const url_params = data_dict['url_params'];
        if(browser){
            // 浏览器替换当前历史记录
            function browser_redirect(){
                goto(url_pathname + url_params, {
                    replaceState: true, // 清除历史记录
                    invalidateAll: true // 重新加载数据
                }).then(r => {
                    //
                });
            }
            browser_redirect();
        }else{
            try {
                // 服务器301永久重定向
                function server_redirect(){
                    throw redirect(301, url_pathname+url_params);
                }
                server_redirect();
            }catch (e){
                console.log("服务端不可用");
            }
        }
    },
    get_agent: function(){
        let that = this;
        //
        return navigator.userAgent;
    },
    get_href: function(){
        let that = this;
        //
        if(browser){
            return page.url.href;
        }else {
            return "";
        }
    },
    get_host: function(){ // 含port
        let that = this;
        //
        if(browser){
            return page.url.host;
        }else {
            return "";
        }
    },
    get_route: function(){ // 获取当前路由，不含参数
        let that = this;
        //
        if(browser){
            let info = page.route;
            if(typeof info === 'string'){
                return info;
            }else if(typeof info === 'object'){
                return info.id;
            }else{
                return that.json_to_string(info);
            }
        }else {
            return "";
        }
    },
    get_params: function(){ // 仅能获取?参数，不能获取#参数，#参数请用search_param()
        let that = this;
        //
        if(browser){
            return page.url.search;
        }else {
            return "";
        }
    },
    search_param: function(key){ // // 获取当前url中的参数
        let that = this;
        //
        return that.search_href_param(that.get_params(), key);
    },
    search_href_param: function (url, key) { // 获取url中的参数
        let that = this;
        // 兼容模式url地址，例如：poop.html?page=3&ok=222#p=2#name=kd
        let url_str = "";
        if(!url){
            url_str = that.get_href();
        } else {
            url_str = url;
        }
        let regExp = new RegExp("([?]|&|#)" + key + "=([^&|^#]*)(&|$|#)");
        let result = url_str.match(regExp);
        if (result) {
            try {
                return decodeURIComponent(result[2]); // 转义还原参数
            }catch (e) {
                return result[2];
            }
        }else {
            return ""; // 没有匹配的键即返回空
        }
    },
    js_rand: function (min, max) { // [min, max]
        return Math.floor(Math.random() * (max - min + 1) + min);
    },
    set_local_data: function (key, value){ // 新增或更新数据（总和最大5M，关闭页面值不会消失。尽量总条数小于50条，每条小于100KB。）。数据持久化请使用func.js_call_py_or_go("set_data", {data_key:"", data_value:"", data_timeout_s:2*365*24*3600}).then(res=>{let data=res.content.data;}); 。
        let that = this;
        key = that.url_encode(key); // 支持中文和特殊字符
        //
        if (browser){
            localStorage.setItem(key,value);
            return localStorage.getItem(key);
        }else{
            return "";
        }
    },
    get_local_data: function (key) { // 获取一个
        let that = this;
        key = that.url_encode(key);
        //
        if (browser){
            let value = localStorage.getItem(key);
            if (value){
                return value;
            }else {
                return "";
            }
        }else{
            return "";
        }
    },
    del_local_data: function (key) { // 删除一个
        let that = this;
        key = that.url_encode(key);
        //
        if (browser){
            return localStorage.removeItem(key);
        }else {
            return false;
        }
    },
    clear_local_data: function () { // 全部清空
        if (browser){
            return localStorage.clear();
        }else {
            return false;
        }
    },
    get_time_s: function () {
        return Math.floor((new Date()).getTime()/1000);
    }, // 秒时间戳，s
    get_time_ms: function(){
        return (new Date()).getTime();
    }, // 毫秒时间戳，ms
    get_time_date: function(format){ // Ymd His
        let that = this;
        return that.get_time_s_date(format, "");
    },
    get_time_s_date: function(format, time_s){ // YmdHisW，日期周
        let that = this;
        let t;
        if (!time_s){
            t = new Date();
        }else {
            t = new Date(time_s*1);
        }
        let seconds = t.getSeconds(); if (seconds<10){seconds = "0"+seconds;}
        let minutes = t.getMinutes(); if (minutes<10){minutes = "0"+minutes;}
        let hour = t.getHours(); if (hour<10){hour = "0"+hour;}
        let day = t.getDate(); if (day<10){day = "0"+day;}
        let month = t.getMonth() + 1; if (month<10){month = "0"+month;}
        let year = t.getFullYear();
        let week = ["week1", "week2", "week3", "week4", "week5", "week6", "week7"][t.getDay()]; // 周

        format = format.replaceAll("Y", year);
        format = format.replaceAll("m", month);
        format = format.replaceAll("d", day);
        format = format.replaceAll("H", hour);
        format = format.replaceAll("i", minutes);
        format = format.replaceAll("s", seconds);
        format = format.replaceAll("W", week);

        return format;
    },
    get_time_ms_format: function (format, time_ms){ // 毫秒时间戳转日期
        let that = this;
        if (!time_ms){
            time_ms = that.get_time_ms();
        }else{
            time_ms = time_ms*1;
        }
        return this.get_time_s_date(format, time_ms);
    },
    format_date: function (new_format, date){ // (只YmdHis格式, 新YmdHis格式)
        date = date+""; // 必须string
        let year = date.slice(0,4);
        let month = date.slice(4,6);
        let day = date.slice(6,8);
        let hour = date.slice(8,10);
        let minutes = date.slice(10,12);
        let seconds = date.slice(12,14);

        let format = new_format;

        format = format.replaceAll("Y", year);
        format = format.replaceAll("m", month);
        format = format.replaceAll("d", day);
        format = format.replaceAll("H", hour);
        format = format.replaceAll("i", minutes);
        format = format.replaceAll("s", seconds);

        return format;
    },
    is_weixin: function (){
        let ua = window.navigator.userAgent.toLowerCase();
        return ua.match(/micromessenger/i) === 'micromessenger';
    },
    is_qq: function (){
        let ua = window.navigator.userAgent.toLowerCase();
        return ((ua.indexOf("qq")!==-1) && !(ua.indexOf("qqbrowser")!==-1));
    },
    is_dingding: function (){
        let ua = window.navigator.userAgent.toLowerCase();
        return ua.indexOf("dingtalk")!==-1;
    },
    is_work_weixin: function (){
        let ua = window.navigator.userAgent.toLowerCase();
        return ua.indexOf("wxwork")!==-1;
    },
    is_feishu: function (){
        let ua = window.navigator.userAgent.toLowerCase();
        return ua.indexOf("lark")!==-1;
    },
    make_uid: function (app_class=""){
        let that = this;
        let rand = that.js_rand(10000000000, 999999999999);
        let ua = window.navigator.userAgent.toLowerCase();
        let lang = (navigator.language?navigator.language:"-").toLowerCase();
        let app_date = that.get_time_date("YmdHisW");
        let href = "";
        if (browser){
            href = window.location.href.toLowerCase();
        }
        return that.md5(app_class+"@"+ua+"@"+app_date+"@"+href+"@"+window.innerWidth+"@"+rand+"@"+lang);
    },
    get_theme_model: function (){ // 获取浏览器当前处于light还是dark
        if (browser){
            let light = window.matchMedia('(prefers-color-scheme: light)').matches;
            if (light){
                return "light";
            }else {
                return "dark";
            }
        }else {
            return "light";
        }
    },
    md5: function (string){
        if (!string){
            return "";
        }else{
            return md5(string);
        }
    },
    base64_encode: function (string) {
        try {
            return btoa(string);
        }catch (e) {
            return "";
        }
    },
    base64_decode: function (string) {
        try {
            return atob(string);
        }catch (e) {
            return "";
        }
    },
    url_encode: function (url) {
        return encodeURIComponent(url);
    },
    url_decode: function (url) {
        return decodeURIComponent(url);
    },
    text_encode: function (text){
        let that = this;
        return that.string_to_unicode(text);
    },
    text_decode: function (text){
        let that = this;
        return that.unicode_to_string(text);
    },
    string_to_unicode: function(string) {
        let that = this;
        // 处理非字符串输入
        if (typeof string !== 'string') {
            string = String(string);
        }
        if (string.length === 0) return "";

        // 使用数组收集编码，然后join，效率更高
        let codes = [""]; // 默认一个空值可以避免多次转换丢失一个值
        for (let i = 0; i < string.length; i++) {
            codes.push(string.charCodeAt(i));
        }
        return codes.join(',');
    },
    unicode_to_string: function(unicode) {
        let that = this;
        // 处理无效输入
        if (unicode === null || unicode === undefined) {
            return "";
        }

        // 如果是数字，直接转换
        if (typeof unicode === 'number') {
            return String.fromCharCode(unicode);
        }

        // 确保是字符串
        unicode = String(unicode).trim();
        if (unicode === "") return "";

        try {
            // 处理逗号分隔的Unicode序列
            if (unicode.indexOf(',') !== -1) {
                let parts = unicode.split(',');
                let result = [];

                for (let i = 0; i < parts.length; i++) {
                    let part = parts[i].trim();
                    // 跳过空部分
                    if (part === "") continue;

                    // 转换为数字
                    let code = Number(part);
                    // 验证是否为有效Unicode码点
                    if (isNaN(code) || code < 0 || code > 0x10FFFF) {
                        // 无效编码，返回原字符串
                        return unicode;
                    }
                    result.push(String.fromCharCode(code));
                }

                return result.join('');
            } else {
                // 处理单个Unicode码点
                let code = Number(unicode);
                let _unicode = "";
                // 验证是否为有效Unicode码点
                if (!isNaN(code) && code >= 0 && code <= 0x10FFFF) {
                    _unicode = String.fromCharCode(code);
                }else{
                    _unicode = unicode;
                }
                // 比较值
                if (that.string_to_unicode(unicode) === unicode){
                    return _unicode;
                }else{
                    return unicode;
                }
            }
        } catch (e) {
            // 任何错误都返回原字符串
            return unicode;
        }
    },
    hex16_to_string: function (hex16) { // 除了不支持emoji外都支持
        return decodeURIComponent(hex16);
    },
    string_to_hex16: function (string){ // 字符串转16进制，任意字符串（中文、emoji）
        let hex = "";
        try {
            for (let i = 0; i < string.length; i++) {
                if (hex){
                    hex += "&#x"+string.charCodeAt(i).toString(16)+";";
                }else{
                    hex = "&#x"+string.charCodeAt(i).toString(16)+";";
                }
            }
            return hex;
        }catch (e) {
            return hex;
        }
    },
    string_to_json: function (string) { // 将string转化为json，注意，里面所有key的引号为双引号，否则浏览器会报错。
        let json;
        let back = string;
        if(typeof back === "string"){
            json = JSON.parse(back);
        } else {
            json = back;
        }

        return json;
    },
    json_to_string: function (json) { // 将json转化为string
        let string;
        let back = json;

        if(typeof back === "object"){
            string = JSON.stringify(back);
        } else {
            string = back;
        }

        return string;
    },
    string_star: function (str, frontLen, endLen) { // //str：要进行隐藏的字符串，frontLen: 前面需要保留几位，endLen: 后面需要保留几位
        let len = str.length - frontLen - endLen;
        let star = "";
        for (let i = 0; i < len; i++) {
            star += "*";
        }
        return (
            str.substring(0, frontLen) + star + str.substring(str.length - endLen)
        );
    },
    // 从 文件地址 获取 目录名 或 文件名。注意win下需要转成mac下的斜杠/
    get_file_ext: function (pathname){
        let array = pathname.split("/");
        if (array.length){
            return array[array.length-1];
        }else{
            return "";
        }
    },
    is_video: function(filename){ // 是视频
        try {
            let ext = filename.substring(filename.lastIndexOf("."));
            ext = ext.toLowerCase();
            let white_ext = [
                ".mp4", ".mkv", ".avi", ".flv", ".mov", ".m4v", ".rmvb", ".rm", ".webm", ".asf", ".wmv",
            ];
            return white_ext.includes(ext);
        }catch (e) {
            return false;
        }
    },
    is_audio: function(filename){ // 是音频
        try {
            let ext = filename.substring(filename.lastIndexOf("."));
            ext = ext.toLowerCase();
            let white_ext = [
                ".mp3", ".wav", ".m3u", ".m4a", ".flac",
            ];
            return white_ext.includes(ext);
        }catch (e) {
            return false;
        }
    },
    is_img: function(filename){ // 是图片
        try {
            let ext = filename.substring(filename.lastIndexOf("."));
            ext = ext.toLowerCase();
            let white_ext = [
                ".gif", ".png", ".jpg", ".jpeg", ".webp", ".ico", ".jpg2", ".tiff", ".tif", ".bmp", ".svg",
            ];
            return white_ext.includes(ext);
        }catch (e) {
            return false;
        }
    },
    is_mobile_screen: function (){ // -1 非法，0 PC，1 mobile
        let width = window.screen.width;
        let height = window.screen.height;
        let max_px = 1280; // 最大 1280X900 px
        let min_px = 200;
        let rate = 40;
        if (width < min_px || height < min_px){ // 非法
            return 0; // -1
        }else{
            if (Math.abs(width-height) < rate){ // 非法
                return 0; // -1
            }else{
                if (width>max_px || height>max_px){
                    return 0; // PC
                }else{
                    return 1; // mobile
                }
            }
        }
    },
    is_pwa: function (){ // 综合判断
        let that = this;
        //
        return (that.is_mobile_pwa() || that.is_pc_pwa() || that.is_wails() || that.is_gthon());
    },
    is_mobile_pwa: function (){ // iOS/Android端pwa，不同浏览器不一定
        return window.navigator?.standalone || document.referrer.includes('android-app://');
    },
    is_pc_pwa: function (){ // win/mac端pwa，不同浏览器不一定
        const displayModes = ['fullscreen', 'standalone', 'minimal-ui'];
        return displayModes.some(
            displayMode => window.matchMedia('(display-mode: ' + displayMode + ')').matches
        );
    },
    html_to_plain_text: function (html) { // string类型的html转换成text
        let that = this;
        function htmlReplaceMediaTags (str, fallback = { // string类型的html里面的全部媒体标签替换成文字
            img: ' [🏞️] ',
            audio: ' [🎵] ',
            video: ' [🎬] '
        }) {
            return str
                .replace(/<img[^>]*alt="([^"]*)"[^>]*>/gi, (match, alt) => " [🏞️ "+alt+"] " || fallback.img)
                .replace(/<audio[^>]*title="([^"]*)"[^>]*>.*?<\/audio>/gi, (match, title) => " [🎵 "+title+"] " || fallback.audio)
                .replace(/<video[^>]*title="([^"]*)"[^>]*>.*?<\/video>/gi, (match, title) => " [🎬 "+title+"] " || fallback.video);
        }
        html = htmlReplaceMediaTags(html);
        //
        let temp = document.createElement('div');
        temp.innerHTML = html;
        return temp.innerText || temp.textContent;
    },
    /**
     * 直接调用go活py的方法
     * @param {string} key 方法名
     * @param {object} data_dict 数据data字典
     * @returns {Promise<object>} 返回固定格式
     */
    js_call_py_or_go: function (key, data_dict){
        let that = this;
        // js远程调用
        const post_request = function (api_url, body_dict) {
            return new Promise(resolve => {
                try {
                    FetchPOST(api_url+"?cache="+that.get_time_ms(), body_dict).then(result=>{
                        resolve(result);
                    });
                } catch (error) {
                    that.notice("Fetch Error 2");
                    console.error('Fetch error 2:', error);
                    resolve({
                        "state": 0,
                        "msg": "请求失败3",
                        "content": {
                            "body_dict": body_dict,
                            "error": error,
                        }
                    });
                }
            });
        };
        //
        return new Promise(resolve => {
            const sys_backend = config.sys.backend; // go、py
            const _app_class = config.app.app_class;
            const _app_version = config.app.app_version;
            //
            let api_url = "";
            let window_token = "";
            if (sys_backend === "py"){
                const _js_call_py_api = that.get_local_data("js_call_py_api");
                const _js_call_py_auth = that.get_local_data("js_call_py_auth");
                if (_js_call_py_api && _js_call_py_auth){
                    api_url = _js_call_py_api + "/" + _js_call_py_auth;
                }else{
                    try {
                        api_url = config.api.js_call_py_url;
                    }catch (e) {
                        api_url = "null-js_call_py_url";
                    }
                }
                window_token = that.get_local_data("window_token");
            }else if (sys_backend === "go"){
                const _js_call_go_api = that.get_local_data("js_call_go_api");
                if (_js_call_go_api){
                    api_url = _js_call_go_api;
                }else{
                    try {
                        api_url = config.api.js_call_go_url;
                    }catch (e) {
                        api_url = "null-js_call_go_url";
                    }
                }
                window_token = that.get_local_data("window_token");
            }else{
                that.notice("config Error");
                resolve({
                    "state": 0,
                    "msg": "config参数错误",
                    "content": {
                        "key": key,
                        "body_dict": {},
                    },
                });
                return
            }
            //
            let body_dict = {
                "window_token": window_token,
                "key": key,
                "data_dict": data_dict,
                "app_class": _app_class,
                "app_version": _app_version,
            }
            //
            try{
                post_request(api_url, body_dict).then(res=>{
                    resolve(res);
                })
            }catch(e){
                resolve({
                    "state": 0,
                    "msg": "JSCallX无此方法",
                    "content": {
                        "key": key,
                        "body_dict": body_dict,
                    },
                });
            }
        });
    },
    js_watch_window_display: function (){ // 显示还是隐藏窗口的状态的判断
        let that = this;

        // // 检查当前页面是否隐藏（最小化或切换标签页）
        // const isMinimized = document.hidden;
        // // 或者使用 visibilityState
        // const isVisible = document.visibilityState === 'visible';
        // const isHidden = document.visibilityState === 'hidden';
        // 添加事件监听器
        document.addEventListener('visibilitychange', () => {
            let display = "hiding";
            if (document.hidden) {
                display = "hiding";
            } else {
                display = "showing";
            }

            //
            const sys_backend = config.sys.backend; // go、py
            if (sys_backend === "py"){
                //
                try{
                    that.js_call_py_or_go("window_display", {"display": display}).then(
                        back_data=>{
                            console.log("[视窗JS-Log]", "js_call_py.py返回值：", back_data);
                        }
                    );
                }catch(e){}
            }

        });
    },
    is_wails: function (){ // 是否是wails环境
        let that = this;
        //
        let agent = that.get_agent().toLowerCase();
        if(browser){
            return agent.indexOf("wails") !== -1 ;
        }else {
            return false;
        }
    },
    is_gthon: function (){ // 是否是gthon环境
        let that = this;
        //
        let agent = that.get_agent().toLowerCase();
        if(browser){
            return agent.indexOf("gthon") !== -1 ;
        }else {
            return false;
        }
    },
    get_lang_index: function (lang){ // 获取语言索引
        let that = this;
        // 将语言转换成可用的数组索引标记
        function make_lang_index(_language){
            if (_language.indexOf("zh") >= 0) { // 简体中文（包含繁体）
                return "zh";
            }
            else if (_language.indexOf("en") >= 0){ // 英文
                return "en";
            }
            else if (_language.indexOf("jp") >= 0){ // 日文
                return "jp";
            }
            else if (_language.indexOf("fr") >= 0){ // 法语
                return "fr";
            }
            else if (_language.indexOf("de") >= 0){ // 德语
                return "de";
            }
            else if (_language.indexOf("ru") >= 0){ // 俄语或乌克兰语
                return "ru";
            }
            else if (_language.indexOf("es") >= 0){ // 西班牙语
                return "es";
            }
            else if (_language.indexOf("ko") >= 0){ // 韩语或朝鲜语
                return "ko";
            }
            else if (_language.indexOf("vi") >= 0){ // 越语
                return "vi";
            }
            else{ // 默认英文
                return "en"
            }
        }
        // 系统语言
        function sys_language(_lang=""){
            if (_lang.length >= 2){
                return _lang.toLowerCase();
            }else {
                if (browser){
                    return navigator.language.toLowerCase();
                }else{
                    return "en";
                }
            }
        }
        //
        return make_lang_index(sys_language(lang))
    },
    get_lang: function (){ // 直接获取lang
        let that = this;
        //
        let lang = "";
        let lang_data = watch_lang_data.lang_index;
        if (lang_data.length >= 2) {
            lang = lang_data
        }
        return that.get_lang_index(lang);
    },
    // 获取翻译
     get_translate: function(key="", lang=""){
        let that = this;
         // 从本地读取语言配置
         if(lang.length >= 2){ // lang参数优先
             // that.console_log("自定义lang=", lang);
         }else{
             let lang_data = watch_lang_data.lang_index;
             if (lang_data.length >= 2) {
                 lang = lang_data
             }
         }
         // 语言标记
         let lang_index = that.get_lang_index(lang);
         // console.log("get_translate=", lang_index, key);
         // console.log("get_translate=", key, lang, sys_language(lang), lang.indexOf("zh"), lang_index);
        //
        if (lang_dict[key]){
            if (lang_dict[key][lang_index]){
                return lang_dict[key][lang_index];
            }else{
                if (lang_dict["_null"][lang_index]){
                    return lang_dict["_null"][lang_index];
                }else{
                    return lang_dict["_null"]["en"]
                }
            }
        }else{
            if (lang_dict["_null"][lang_index]){
                return lang_dict["_null"][lang_index];
            }else{
                return lang_dict["_null"]["en"]
            }
        }
    },
    open_url: function (url="", target="_self"){ // 需要强制刷新所有数据时，请勿使用此函数
        let that = this;
        if (browser){
            if (url.length >= 1){
                if (target === "_self"){
                    goto(url, {
                        replaceState: true, // false新增历史记录，true清除历史记录
                        invalidateAll: true, // true强制重新加载
                        noScroll: true // true回到滚动位置
                    }).then(r => {
                        //
                    });
                }else {
                    window.open(url, target);
                }
            }else{
                //
            }
        }else{
            //
        }
    },
    open_url_no_cache: function (url="./?reload=no-cache", target="_self"){ // 强制刷新页面或跳转或更新页面全部数据，仅针对ssr=true时
        let that = this;
        if (browser){
            // url请携带新参数
            if (url.length >= 1){
                if (target === "_self"){
                    history.replaceState(null, '', url);
                    window.location.replace(url);
                }else {
                    history.replaceState(null, '', url);
                    window.open(url, target);
                }
            }else{
                //
            }
        }else{
            //
        }
    },
    open_url_with_default_browser: function (url=""){ // 用系统浏览器打开链接
        let that = this;
        //
        let target = "_blank";
        if (that.is_gthon() || that.is_wails()){
            that.js_call_py_or_go("open_url_with_default_browser", {
                lang: that.get_lang(),
                url: url,
                target: target,
            }).then(result => {});
        }else{
            that.open_url(url, target);
        }
    },
    fresh_page: function (timeout_ms=500){
        let that = this;
        if (timeout_ms<=0){
            timeout_ms = 0;
        }
        if (browser){
            setTimeout(function(){
                window.location.reload();
                // that.open_url(that.get_href(), "_self");
            }, timeout_ms);
        }else {
            //
        }
    },
    get_app_uid: function (){ // 随机app_uid
        let that = this;
        //
        let app_uid_key = config.app.app_class+"app_uid";
        return new Promise(resolve => {
            func.js_call_py_or_go("get_data", {data_key:app_uid_key}).then(res=>{
                let _app_uid=res.content.data;
                if (_app_uid){
                    app_uid_data.app_uid = _app_uid;
                    resolve(_app_uid);
                }else{
                    _app_uid = that.md5(that.make_uid(config.app.app_class));
                    func.js_call_py_or_go("set_data", {data_key:app_uid_key, data_value:_app_uid, data_timeout_s:10*365*24*3600}).then(res=>{
                        app_uid_data.app_uid = res.content.data;
                        resolve(res.content.data);
                    });
                }
            });
        });
    },
    ping: function (url) {
        let that = this;
        //
        return new Promise((resolve, reject) => {
            FetchGET(url, {}, 5).then(result => {
                let state = 0;
                let msg  = "";
                if (result.state !== 404) {
                    state = 1;
                    msg  = "接口访问成功，但status状态可能是200、30X。";
                } else {
                    state = 404;
                    msg  = "超时或者接口无效。";
                }
                resolve({
                    state: state,
                    msg: msg,
                    result: result,
                });
            }).catch(err=>{
                resolve({
                    state: 404,
                    msg: "",
                    result: {},
                });
            });
        });
    },
    set_db_data: function (key, value) { // 健值对方式存储数据到indexDB，单条大小无限制。数据持久化请使用func.js_call_py_or_go("set_data", {data_key:"", data_value:"", data_timeout_s:2*365*24*3600}).then(res=>{let data=res.content.data;}); 。
        let that = this;
        //
        key = that.url_encode(key)
            .replaceAll("%", "_")
            .replaceAll("$", "-")
            .replaceAll("!", "_-")
            .replaceAll("^", "_-");
        let data_dict_array = [
            {
                only_key: key,
                any_type_value: value,
                update_time: that.get_time_s_date("YmdHis")*1,  // 使用时间戳
                remark: "func-set",
            }
        ];
        return new Promise((resolve) => {
            dexie_kv_db.update_db_data(data_dict_array).then(ids_array => {
                if (ids_array.length >= 1){
                    that.get_db_data(key).then(value=>{
                        resolve(value);
                    });
                }else{
                    resolve("");
                }
            });
        });
    },
    get_db_data: function (key){
        let that = this;
        //
        key = that.url_encode(key)
            .replaceAll("%", "_")
            .replaceAll("$", "-")
            .replaceAll("!", "_-")
            .replaceAll("^", "_-");
        return new Promise((resolve) => {
            dexie_kv_db.get_db_data(key).then(result => {
                if (result){
                    resolve(result.any_type_value);
                }else{
                    resolve("");
                }
            });
        });
    },
    del_db_data: function (key){
        let that = this;
        //
        key = that.url_encode(key)
            .replaceAll("%", "_")
            .replaceAll("$", "-")
            .replaceAll("!", "_-")
            .replaceAll("^", "_-");
        return new Promise((resolve) => {
            dexie_kv_db.del_db_data(key).then(state => {
                resolve(state);
            });
        });
    },
    //
    converted_path: function (path = ""){ // 路径转成标准路径
        path = path.replaceAll("\\", "/");
        path = path.replaceAll("//", "/");
        if (path.endsWith('/')) { // 删除最后一位是/
            path = path.slice(0, -1);
        }
        return path;
    },
    filepath_to_filename: function(filepath = ""){ // 把目录或带目录的文件换成称呼
        let that = this;
        //
        filepath = that.converted_path(filepath);
        let filepath_array = filepath.split("/");
        if (filepath.length > 0 && filepath){
            return filepath_array[filepath_array.length - 1];
        }else{
            return "";
        }
    },
    replaceLast: function (text, search, replacement) { // 替换字符串最后一个出现的小字符串
        const lastIndex = text.lastIndexOf(search);
        if (lastIndex === -1) {
            return text; // 没有找到匹配项
        }
        return text.substring(0, lastIndex) + replacement + text.substring(lastIndex + search.length);
    },
    loading_show: function(msg="", timeout_ms = "long"){
        let that = this;
        //
        clearTimeout(loading_show_timer);
        loading_data.loading_show = "show";
        loading_data.loading_msg = msg;
        if (timeout_ms === "long"){
            // 长时间显示
        }else{
            if (timeout_ms <= 200){
                timeout_ms = 200;
            }
            //
            loading_show_timer = setTimeout(function () {
                that.loading_hide();
            }, timeout_ms);
        }
    },
    loading_hide: function(){
        clearTimeout(loading_show_timer);
        loading_data.loading_show = "hide";
        loading_data.loading_msg = "";
    },
    alert_msg: function (msg, timeout_ms){
        clearTimeout(alert_msg_timer);
        alert_data.alert_show = "show";
        alert_data.alert_msg = msg;
        if (timeout_ms === "long"){
            // 长时间显示
        }else{
            if (timeout_ms <= 200){
                timeout_ms = 200;
            }
            //
            //
            alert_msg_timer = setTimeout(function () {
                alert_data.alert_show = "hide";
                alert_data.alert_msg = "";
            }, timeout_ms);
        }
    },
    notice: function (title="", msg="", timeout_ms = 5000, trigger="info"){
        if (timeout_ms <= 200){
            timeout_ms = 200;
        }
        switch (trigger) {
            case "info":
                notice_data.toaster.info({
                    title: title,
                    description: msg,
                    duration: timeout_ms,
                });
                break;
            case "warn" || "warning":
                notice_data.toaster.warning({
                    title: title,
                    description: msg,
                    duration: timeout_ms,
                });
                break;
            case "error":
                notice_data.toaster.error({
                    title: title,
                    description: msg,
                    duration: timeout_ms,
                });
                break;
            default:
                notice_data.toaster.info({
                    title: title,
                    description: msg,
                    duration: timeout_ms,
                });
                break;
        }
    },
    change_window_size: function(){
        let that = this;
        //
        if (size_tag === "size_init"){
            size_tag = "size_full_height";
        }else if (size_tag === "size_full_height"){
            size_tag = "size_full_window"; // 上下左右对齐，非全屏
        }else{
            size_tag = "size_init";
        }
        //
        that.js_call_py_or_go("change_window_size", {
            size_tag: size_tag,
            width: 0,
            height: 0
        }).then(res=>{
            console.log("change_window_size=", res);
        });
    },
    //
    open_url_404: function (root_route="./", error_msg="", error_url=""){ // 规范打开404页面，root_route根据页面所在路由计算
        let that = this;
        //
        let href = root_route+"_404?error_msg="+encodeURIComponent(error_msg)+"&error_url=" + encodeURIComponent(error_url);
        that.open_url(href, "_self");
    },
    url_timeout_encode: function (route, timeout){ // 生成url的时间戳标记， timeout=s
        let that = this;
        let mark = route+"#@"+that.get_time_s()+"#@"+timeout;
        return encodeURIComponent(that.string_to_unicode(mark+"#@"+that.md5(mark)+"#@"+that.js_rand(10000000, 9999999999)));
    },
    url_timeout_decode: function (route, url_timeout){ // true未过期，false过期
        let that = this;
        let now_time = that.get_time_s();
        try {
            let param = decodeURIComponent(that.unicode_to_string(url_timeout));
            let array = param.split("#@");
            //
            let len = now_time-array[1]*1;
            let _route = array[0];
            let timeout = array[2]*1;
            let mark_md5 = array[3];
            let mark = array[0]+"#@"+array[1]+"#@"+array[2];
            if (route === _route && mark_md5 === that.md5(mark)){
                return len <= timeout && len >= 0;
            }else{
                return false;
            }
        }catch (e) {
            return false;
        }
    },
    is_localhost: function (ip=""){ // ipv4、ipv6是否是本地IP
        let hostname = ip;
        if (browser){
            if (!hostname){hostname = window.location.hostname;}
            hostname = hostname.toLowerCase();
            return hostname === 'localhost' ||
                hostname.includes('localhost') ||
                hostname === '127.0.0.1' ||
                hostname === '[::1]' ||  // IPv6 localhost
                hostname === '0.0.0.0';
        }else{
            return false;
        }
    },
    is_local_ipv4: function (ip=""){
        let hostname = ip;
        if (browser){
            if (!hostname){hostname = window.location.hostname;}
            hostname = hostname.toLowerCase();
            return hostname.startsWith('192.168.') ||
                hostname.startsWith('10.') ||
                hostname.startsWith('172.') ||
                hostname.startsWith('169.254.') || // 链路本地
                hostname === 'localhost' ||
                hostname.includes('localhost') ||
                hostname === '127.0.0.1';
        }else{
            return false;
        }
    },
    is_local_ipv6: function (ip=""){
        let hostname = ip;
        if (browser){
            if (!hostname){hostname = window.location.hostname;}
            hostname = hostname.toLowerCase();
            return hostname === '::1' ||
                hostname.startsWith('fe80:') ||
                hostname.startsWith('fc') ||
                hostname.startsWith('fd');
        }else{
            return false;
        }
    },
    is_url: function (string=""){ // http(s) ftp(s) file
        string = string.toLowerCase();
        if (
            string.indexOf("http:") === 0
            || string.indexOf("https:") === 0
            || string.indexOf("ftp:") === 0
            || string.indexOf("ftps:") === 0
            || string.indexOf("file:") === 0
            // || string.indexOf("view-source:") === 0
            || string.indexOf("mailto:") === 0
            || string.indexOf("rtsp:") === 0
            || string.indexOf("tel:") === 0
            || string.indexOf("sms:") === 0
        ){ // 严格限制协议开头
            try {
                new URL(string);
                return true;
            } catch (err) {
                return false;
            }
        }else{
            return false;
        }
    },
    watch_input_enter: function(input_object){ // 监测输入法是否已经输入完成，请将此函数放置在page_start()里面或on Mount的runtime_ok后面
        // 判断用户输入框是否已经输入完成。 1直接完成输入，2预选词输入完成，-1开始输入，0词预选状态。1和2都是输入完成，请区分具体数值。
        // 1️⃣let input_object: any; // input标签dom对象
        // 2️⃣bind:this={input_object} // 获取当前input_object对象
        // 3️⃣func.watch_input_enter(input_object); // 监听输入法输入事件
        // 4️⃣def.input_enter(){执行具体Enter回调}
        if (browser){
            //
            input_object.addEventListener('compositionstart',function(e){
                input_enter_data.input_doing = -1;
                // console.log("compositionstart=", input_enter_data.input_doing);
            },false);
            input_object.addEventListener('input',function(e){
                if (input_enter_data.input_doing === -1){ // 词预选状态
                    input_enter_data.input_doing = 0;
                } else if (input_enter_data.input_doing === 1 || input_enter_data.input_doing === 2) { // 直接输入状态，顺便初始化input_doing
                    input_enter_data.input_doing = 1;
                } else {
                    input_enter_data.input_doing = 0;
                }
                // console.log("input=", input_enter_data.input_doing);
            },false);
            input_object.addEventListener('compositionend',function(e){
                if (input_enter_data.input_doing === 0){ // 预选词已确定时触发
                    input_enter_data.input_doing = 2;
                }else if (input_enter_data.input_doing === 1) { // 输入完成时触发
                    input_enter_data.input_doing = 1;
                }else {
                    input_enter_data.input_doing = 0;
                }
                // console.log("compositionend=", input_enter_data.input_doing);
            },false);
        }else{
            console.warn("此方法只适用于浏览器:input_enter_complete");
        }
    },
    make_qr_base64: function (txt="", width=200, height=200){
        // npm install qrcode
        return new Promise(resolve => {
            QRCode.toDataURL(txt.trim(), {
                // 二维码大小和边距
                width: width,           // 二维码宽度（像素）
                height: height,          // 二维码高度（像素）
                margin: 3,           // 二维码边距（像素）
                // 颜色配置
                color: {
                    dark: '#426BE9',    // 暗色模块颜色（默认黑色）
                    light: '#FEFEFE'    // 亮色模块颜色（默认白色）
                },
                // 纠错级别
                errorCorrectionLevel: 'H', // L, M, Q, H
                // 二维码版本（1-40）
                version: 0,
                // 掩码模式（0-7）
                maskPattern: 2,
                // 输出格式
                type: 'image/png',    // 也可以是 'image/jpeg', 'image/webp'
                quality: 0.92,        // 仅对 JPEG/WebP 有效
                // 渲染器选项
                rendererOpts: {
                    quality: 1          // PNG 质量
                }
            })
            .then(base64 => {
                resolve(base64);
            });
        });
    },
    support_min_os: function(customUserAgent="") { // 【慎用，因为有些PC浏览器的规则并不适用】 true通过，false不通过。最低支持：Android10、iOS16、iPadOS16、MacOS14、Win10、鸿蒙6、Linux(2024年3月+)
        const ua = (customUserAgent || navigator.userAgent).toLowerCase();

        // 版本号转数值阶梯：支持语义化版本比较，如 "16.1.2" -> 16.0102
        const versionToNumeric = (versionStr) => {
            if (!versionStr) return 0;
            const parts = versionStr.split('.').map(Number);
            return (parts[0] || 0) +
                ((parts[1] || 0) / 100) +
                ((parts[2] || 0) / 10000);
        };

        // 版本比较（带浮点数精度容差）
        const versionGte = (current, required) => current >= required - 0.0001;

        // 最低版本要求（数值化）
        const MIN_VERSIONS = {
            android: versionToNumeric('10'),
            ios: versionToNumeric('16'),
            ipados: versionToNumeric('16'),
            macos: versionToNumeric('14'),
            windows: versionToNumeric('10'),
            harmonyos: versionToNumeric('6'),
            linux: versionToNumeric('2024.3')  // 2024年3月
        };

        // Linux发行版版本到发布日期的完整映射
        const DISTRO_RELEASE_DATES = {
            // Ubuntu
            ubuntu: {
                '20.04': 2020.04, '20.10': 2020.10,
                '21.04': 2021.04, '21.10': 2021.10,
                '22.04': 2022.04, '22.10': 2022.10,
                '23.04': 2023.04, '23.10': 2023.10,
                '24.04': 2024.04, '24.10': 2024.10,
                '25.04': 2025.04
            },
            // Debian
            debian: {
                '10': 2019.07, '10.0': 2019.07, 'buster': 2019.07,
                '11': 2021.08, '11.0': 2021.08, 'bullseye': 2021.08,
                '12': 2023.06, '12.0': 2023.06, 'bookworm': 2023.06,
                '13': 2025.00, '13.0': 2025.00, 'trixie': 2025.00
            },
            // Fedora
            fedora: {
                '37': 2022.11, '38': 2023.04, '39': 2023.11,
                '40': 2024.04, '41': 2024.10, '42': 2025.04
            },
            // RHEL/CentOS
            rhel: {
                '8.6': 2022.05, '8.7': 2022.11, '8.8': 2023.05, '8.9': 2023.11,
                '9.0': 2022.05, '9.1': 2022.11, '9.2': 2023.05, '9.3': 2023.11, '9.4': 2024.05,
                '9.5': 2024.11, '10.0': 2025.00
            },
            // openSUSE
            suse: {
                '15.4': 2022.06, '15.5': 2023.06, '15.6': 2024.06,
                'tumbleweed': 999.0  // 滚动发行版
            },
            // Alpine
            alpine: {
                '3.16': 2022.05, '3.17': 2022.11, '3.18': 2023.05,
                '3.19': 2023.12, '3.20': 2024.05, '3.21': 2024.12
            },
            // 滚动发行版
            arch: { 'default': 999.0 },
            gentoo: { 'default': 999.0 }
        };

        // Linux发行版检测规则
        const LINUX_DISTRO_RULES = [
            { name: 'ubuntu', pattern: /ubuntu[\/\s]([\d.]+)/i },
            { name: 'debian', pattern: /debian[\/\s]([\d]+|bookworm|bullseye|trixie|buster)/i },
            { name: 'fedora', pattern: /fedora[\/\s]([\d]+)/i },
            { name: 'rhel', pattern: /(?:rhel|centos|red hat)[\/\s]?(?:linux[\/\s])?([\d.]+)/i },
            { name: 'suse', pattern: /(?:suse|opensuse)[\/\s]?(?:leap[\/\s])?([\d.]+|tumbleweed)/i },
            { name: 'alpine', pattern: /alpine[\/\s]([\d.]+)/i },
            { name: 'arch', pattern: /arch/i },
            { name: 'gentoo', pattern: /gentoo/i }
        ];

        // Linux内核版本 → 发布日期映射
        const KERNEL_RELEASE_DATES = {
            '6.2': 2023.02, '6.3': 2023.04, '6.4': 2023.06, '6.5': 2023.08,
            '6.6': 2023.10, '6.7': 2024.01, '6.8': 2024.03, '6.9': 2024.05,
            '6.10': 2024.07, '6.11': 2024.09, '6.12': 2024.11,
            '6.13': 2025.01, '6.14': 2025.03
        };

        // 内核版本转发布日期
        const kernelToReleaseDate = (kernelVer) => {
            if (!kernelVer) return 0;
            const majorMinor = kernelVer.match(/(\d+\.\d+)/)?.[1];
            if (!majorMinor) return 0;

            // 精确匹配
            if (KERNEL_RELEASE_DATES[majorMinor]) return KERNEL_RELEASE_DATES[majorMinor];

            // 估算
            const [major, minor] = majorMinor.split('.').map(Number);
            if (major === 6) return 2022 + (minor * 0.2);
            if (major === 5) return 2019 + (minor * 0.3);
            return 0;
        };

        // 获取发行版的发布日期
        const getDistroReleaseDate = (distroName, versionStr) => {
            const distroMap = DISTRO_RELEASE_DATES[distroName];
            if (!distroMap) return 0;

            // 直接匹配版本
            if (distroMap[versionStr]) return distroMap[versionStr];

            // 尝试匹配主版本号
            const majorVersion = versionStr.split('.')[0];
            if (distroMap[majorVersion]) return distroMap[majorVersion];

            // 尝试匹配默认值
            if (distroMap['default']) return distroMap['default'];

            return 0;
        };

        // --- Windows检测 ---
        const winMatch = ua.match(/windows nt ([\d.]+)/);
        if (winMatch) {
            const winVer = versionToNumeric(winMatch[1]);
            if (versionGte(winVer, MIN_VERSIONS.windows)) return true;
        }

        // --- macOS检测 ---
        const macMatch = ua.match(/mac os x ([\d_]+)/) || ua.match(/macintosh; .*? os ([\d_]+)/);
        if (macMatch) {
            const macVer = versionToNumeric(macMatch[1].replace(/_/g, '.'));
            if (versionGte(macVer, MIN_VERSIONS.macos)) return true;
        }

        // --- iOS/iPadOS检测 ---
        const iosMatch = ua.match(/iphone os ([\d_]+)/) || ua.match(/ipad; cpu os ([\d_]+)/);
        if (iosMatch) {
            const iosVer = versionToNumeric(iosMatch[1].replace(/_/g, '.'));
            const minVer = ua.includes('ipad') ? MIN_VERSIONS.ipados : MIN_VERSIONS.ios;
            if (versionGte(iosVer, minVer)) return true;
        }

        // --- Android检测 ---
        const androidMatch = ua.match(/android ([\d.]+)/);
        if (androidMatch && versionGte(versionToNumeric(androidMatch[1]), MIN_VERSIONS.android)) return true;

        // --- 鸿蒙检测 ---
        const harmonyMatch = ua.match(/harmony(?:os)?[\s\/]?([\d.]+)/) || ua.match(/hongmeng[\s\/]?([\d.]+)/);
        if (harmonyMatch && versionGte(versionToNumeric(harmonyMatch[1]), MIN_VERSIONS.harmonyos)) return true;

        // --- Linux检测 ---
        if (ua.includes('linux') && !ua.includes('android')) {
            // 提取内核版本
            const kernelMatch = ua.match(/linux ([\d.]+)/) || ua.match(/kernel ([\d.]+)/);
            const kernelVer = kernelMatch?.[1];
            const kernelDate = kernelToReleaseDate(kernelVer);

            // 检测发行版并获取发布日期
            let maxReleaseDate = 0;
            let detectedDistro = null;

            for (const rule of LINUX_DISTRO_RULES) {
                const match = ua.match(rule.pattern);
                if (match) {
                    detectedDistro = rule.name;
                    const versionStr = match[1] || '';
                    const releaseDate = getDistroReleaseDate(rule.name, versionStr);
                    maxReleaseDate = Math.max(maxReleaseDate, releaseDate);
                }
            }

            // 判断条件：发行版发布日期 >= 2024.3 或 内核发布日期 >= 2024.3
            if (maxReleaseDate > 0 && versionGte(maxReleaseDate, MIN_VERSIONS.linux)) return true;
            if (kernelDate > 0 && versionGte(kernelDate, MIN_VERSIONS.linux)) return true;

            // 通用内核版本检查（6.8+）
            if (kernelVer) {
                const [major, minor] = kernelVer.split('.').map(Number);
                if (major > 6 || (major === 6 && minor >= 8)) return true;
            }

            return false;
        }

        return false;
    },
    support_min_js: function (){ // 最低js支持到ES202x
        // 大致最低支持范围:
        // ES2023，Chrome110+，Firefox115+，iOS16.4+，Android14+，MacOS14+，Win10 2023 Update+，nodeJS20+，Bun0.6+
        // ES2024，Chrome124+，Firefox128+，iOS17.4+，Android16+，MacOS14+，Win10 2024 Update+，nodeJS22+，Bun1.1+
        let that = this;
        //
        const support_es2023 = function (){
            try { // es2023
                return !!(
                    Array.prototype.toSorted &&
                    Array.prototype.toReversed &&
                    Array.prototype.with &&
                    Array.prototype.findLast &&
                    // ES2023 还允许使用 Symbol 作为 WeakMap 的 key
                    (typeof WeakMap !== 'undefined' && (() => {
                        try {
                            const wm = new WeakMap();
                            wm.set(Symbol('test'), 1);
                            return true;
                        } catch (e) {
                            return false;
                        }
                    })())
                );
            } catch (e) {
                return false;
            }
        };
        const support_es2024 = function (){
            try { // es2024
                return !!(
                    // 1. Object.groupBy (最常用的新特性)
                    Object.groupBy &&
                    // 2. Promise.withResolvers (改变 Promise 写法的特性)
                    Promise.withResolvers &&
                    // 3. ArrayBuffer.prototype.resize (内存管理增强)
                    ArrayBuffer.prototype.resize &&
                    // 4. 正则表达式 v 标记 (Unicode 增强)
                    new RegExp('', 'v') &&
                    // 5. Atomics.waitAsync (多线程同步增强)
                    typeof Atomics !== 'undefined' && Atomics.waitAsync
                );
            } catch (e) {
                return false;
            }
        };
        //
        if (!support_es2024() && !support_es2023){
            console.error("support_min_js=", ["es2023", support_es2023()], ["es2024", support_es2024()]);
        }
        //
        if (that.is_gthon() || that.is_wails()){
            return support_es2024();
        }else{
            return support_es2023();
        }
    },
    block_all_script: function (){ // 禁用所有js脚本或禁止继续添加js脚本
        // 禁用所有脚本
        Object.defineProperty(document, 'scripts', {
            get: () => []
        });

        // 阻止新脚本添加
        const observer = new MutationObserver((mutations) => {
            mutations.forEach(mutation => {
                mutation.addedNodes.forEach(node => {
                    if (node.nodeName === 'SCRIPT') {
                        node.remove();
                    }
                });
            });
        });

        observer.observe(document.documentElement, {
            childList: true,
            subtree: true
        });

        // 停止执行
        throw new Error('脚本已被拦截');
    },

    //
}

export default func;