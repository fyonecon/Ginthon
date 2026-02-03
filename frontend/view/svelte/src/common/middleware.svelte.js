// 中间件

import {browser} from "$app/environment";

const runtime_func = {
    browser_fn_state: function (){
        return !(navigator.webdriver || !window.localStorage || !window.indexedDB);
    },
    screen_state: function (){
        if (browser){
            let inner_w = window.innerWidth;
            let inner_h = window.innerHeight;
            let screen_w = window.screen.width;
            let screen_h = window.screen.height;
            //
            return !(inner_w < 220 || inner_h < 220 || screen_w < 220 || screen_h < 220);
        }else{
            return true;
        }
    },
};

const browser_func = {
    is_weixin: function (){
        if (browser){
            let ua = window.navigator.userAgent.toLowerCase();
            return ua.indexOf("micromessenger")!==-1;
        }else{
            return false;
        }
    },
    is_qq: function (){
        if (browser){
            let ua = window.navigator.userAgent.toLowerCase();
            return ((ua.indexOf("qq")!==-1) && !(ua.indexOf("qqbrowser")!==-1));
        }else{
            return false;
        }
    },
    is_dingding: function (){
        if (browser){
            let ua = window.navigator.userAgent.toLowerCase();
            return ua.indexOf("dingtalk")!==-1;
        }else{
            return false;
        }
    },
    is_work_weixin: function (){
        if (browser){
            let ua = window.navigator.userAgent.toLowerCase();
            return ua.indexOf("wxwork")!==-1;
        }else{
            return false;
        }
    },
    is_feishu: function (){
        if (browser){
            let ua = window.navigator.userAgent.toLowerCase();
            return ua.indexOf("lark")!==-1;
        }else{
            return false;
        }
    },
};

/**
 *  page运行时检测，拦截爬虫、审核等
 * @returns {boolean} 返回固定格式
 */
export const runtime_ok = function (){
    return (runtime_func.browser_fn_state() && runtime_func.screen_state());
}

/**
 *  page运行时检测，拦截爬虫、审核等
 * @returns {boolean} 返回固定格式
 */
export const browser_ok = function (){
    return !(browser_func.is_weixin() || browser_func.is_work_weixin() || browser_func.is_qq() || browser_func.is_feishu() || browser_func.is_dingding());
}