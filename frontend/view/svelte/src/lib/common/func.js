import { redirect } from "@sveltejs/kit";
import { goto } from '$app/navigation';
import { page } from '$app/state';
import { browser } from '$app/environment';

const func = {
    test: function(data_dict){
        let that = this;
        console.log("test=", data_dict);
    },
    redirect_pathname: function (data_dict){ // 重定向到新路由。 url_pathname开头/
        let that = this;
        //
        const url_pathname = data_dict['url_pathname'];
        const url_param = data_dict['url_param'];
        if(browser){
            // 浏览器替换当前历史记录
            function browser_redirect(){
                goto(url_pathname + url_param, {replaceState: true}).then(r => {
                    //
                });
            }
            browser_redirect();
        }else{
            try {
                // 服务器301永久重定向
                function server_redirect(){
                    throw redirect(301, url_pathname+url_param);
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
            return page.route;
        }else {
            return "";
        }
    },
    get_param: function(){
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
        let regExp = new RegExp("([?]|&|#)" + key + "=([^&|^#]*)(&|$|#)");
        let result = that.get_param().match(regExp);
        if (result) {
            return decodeURIComponent(result[2]); // 转义还原参数
        }else {
            return ""; // 没有匹配的键即返回空
        }
    },



    //
}

export default func;