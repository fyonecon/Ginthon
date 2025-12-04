import { redirect } from "@sveltejs/kit";
import { goto } from '$app/navigation';
import { page } from '$app/state';
import { browser } from '$app/environment';
import md5 from 'md5';
import { setContext, getContext } from 'svelte';
import config from "$lib/common/config.js";

// 复用函数
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
    url_path: function(pathname){ // URL的path路径前缀，适配后端服务器输出规则。默认""，推荐"."。pathname开头/ 。
        return "."+pathname;
    },
    redirect_pathname: function (data_dict){ // 重定向到新路由。 url_pathname开头/
        let that = this;
        //
        const url_pathname = data_dict['url_pathname'];
        const url_params = data_dict['url_params'];
        if(browser){
            // 浏览器替换当前历史记录
            function browser_redirect(){
                goto(url_pathname + url_params, {replaceState: true}).then(r => {
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
    get_href: function(){
        let that = this;
        //
        if(browser){
            return page.url.href;
        }else {
            return "";
        }
    },
    get_route: function(){
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
    get_params: function(){
        let that = this;
        //
        if(browser){
            return page.url.search;
        }else {
            return "";
        }
    },
    search_param: function(key){
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
            return decodeURIComponent(result[2]); // 转义还原参数
        }else {
            return ""; // 没有匹配的键即返回空
        }
    },
    js_rand: function (min, max) { // [min, max]
        return Math.floor(Math.random() * (max - min + 1) + min);
    },
    set_local_data: function (key, value){ // 新增或更新数据（总和最大4M，关闭页面值不会消失）
        let that = this;
        key = that.url_encode(key); // 支持中文和特殊字符
        //
        localStorage.setItem(key,value);
        return localStorage.getItem(key);
    },
    get_local_data: function (key) { // 获取一个
        let that = this;
        key = that.url_encode(key);
        //
        let value = localStorage.getItem(key);
        if (value){
            return value;
        }else {
            return "";
        }
    },
    del_local_data: function (key) { // 删除一个
        let that = this;
        key = that.url_encode(key);
        //
        return localStorage.removeItem(key);
    },
    clear_local_data: function () { // 全部清空
        return localStorage.clear();
    },
    set_page_data: function(key, value){ // 新增或更新数据（跨路由<页面>值，除非在浏览器关闭页面或刷新页面）
        let that = this;
        key = that.url_encode(key); // 支持中文和特殊字符
        //
        return setContext(key, value);
    },
    get_page_data: function(key){
        let that = this;
        key = that.url_encode(key);
        //
        return getContext(key);
    },
    del_page_data: function(key){
        let that = this;
        key = that.url_encode(key);
        //
        return that.set_page_data(key, null);
    },
    get_time_s: function () {
        return Math.floor((new Date()).getTime()/1000);
    }, // 秒时间戳，s
    get_time_ms: function(){
        return (new Date()).getTime();
    }, // 毫秒时间戳，ms
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
        return ua.indexOf("ding talk")!==-1;
    },
    is_work_weixin: function (){
        let ua = window.navigator.userAgent.toLowerCase();
        return ua.indexOf("wxwork")!==-1;
    },
    is_feishu: function (){
        let ua = window.navigator.userAgent.toLowerCase();
        return ua.indexOf("lark")!==-1;
    },
    make_uid: function (app_class){
        let that = this;
        let rand = that.js_rand(10000000000, 999999999999);
        let ua = window.navigator.userAgent.toLowerCase();
        let app_date = that.time_date("YmdHisW");
        let href = window.location.href.toLowerCase();
        return [that.md5(app_class+"@"+ua+"@"+app_date+"@"+href+"@"+window.innerWidth+"@"+rand), app_date];
    },
    get_theme_model: function (){ // 获取浏览器当前处于light还是dark
        let light = window.matchMedia('(prefers-color-scheme: light)').matches;
        if (light){
            return "light";
        }else {
            return "dark";
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
    string_to_unicode: function (string){ // 字符串转unicode，任意字符串
        let back = "";
        for (let i=0; i<string.length; i++){
            if (back){
                back += ","+string.charCodeAt(i);
            }else{
                back = string.charCodeAt(i);
            }

        }
        return back;
    },
    unicode_to_string: function (unicode){
        const _unicode = unicode.split(",");
        let back = "";
        for (let i=0; i<_unicode.length; i++){
            back += String.fromCharCode(_unicode[i]);
        }
        return back;
    },
    hex16_to_string: function (hex16) { // 除了不支持emoji外都支持
        return decodeURIComponent(hex16);
    },
    string_to_hex16: function (string){ // 字符串转16进制，任意字符串（中文、emoji）
        let hex = "";
        for (let i = 0; i < string.length; i++) {
            if (hex){
                hex += "&#x"+string.charCodeAt(i).toString(16)+";";
            }else{
                hex = "&#x"+string.charCodeAt(i).toString(16)+";";
            }
        }
        return hex;
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
        let ext = filename.substring(filename.lastIndexOf("."));
        ext = ext.toLowerCase();
        let white_ext = [
            ".mp4", ".mkv", ".avi", ".flv", ".mov", ".m4v", ".rmvb", ".rm", ".webm", ".asf", ".wmv",
        ];
        return white_ext.includes(ext);
    },
    is_audio: function(filename){ // 是音频
        let ext = filename.substring(filename.lastIndexOf("."));
        ext = ext.toLowerCase();
        let white_ext = [
            ".mp3", ".wav", ".m3u", ".m4a", ".flac",
        ];
        return white_ext.includes(ext);
    },
    is_img: function(filename){ // 是图片
        let ext = filename.substring(filename.lastIndexOf("."));
        ext = ext.toLowerCase();
        let white_ext = [
            ".gif", ".png", ".jpg", ".jpeg", ".webp", ".ico", ".jpg2", ".tiff", ".tif", ".bmp", ".svg",
        ];
        return white_ext.includes(ext);
    },
    is_mobile_screen: function (){ //-1非法，0PC，1mobile
        let width = window.screen.width;
        let height = window.screen.height;
        let max_px = 1280; // 最大 1280X900 px
        let min_px = 280;
        let rate = 40;
        if (width < min_px || height < min_px){
            return -1;
        }else{
            if (Math.abs(width-height) < rate){
                return -1;
            }else{
                if (width>max_px || height>max_px){
                    return 0;
                }else{
                    return 1;
                }
            }
        }
    },
    is_mobile_pwa: function (){ // iOS/Android端pwa
        return window.navigator?.standalone || document.referrer.includes('android-app://');
    },
    is_pc_pwa: function (){ // win/mac端pwa
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

    //
}

export default func;