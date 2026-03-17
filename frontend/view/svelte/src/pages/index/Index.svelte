<script lang="ts">
    /*根路由*/
    import { resolve } from '$app/paths';
    import func from "../../common/func.svelte.js";
    import {afterNavigate} from "$app/navigation";
    import {onMount} from "svelte";
    import {browser_ok, runtime_ok} from "../../common/middleware.svelte";
    import {browser} from "$app/environment";
    import config from "../../config";


    // 本页面参数
    let route = $state(func.get_route());
    let href = $state(func.get_href());
    let host = $state(config.sys.base_route+"/");
    if (browser){
        host = "//"+window.location.host+config.sys.base_route+"/";
    }


    // 本页面函数：Svelte的HTML组件onXXX=中正确调用：={()=>def.xxx()}
    const def = {
        go_home: function(){
            // 重新定向 /到 /home 页面
            func.redirect_pathname({
                url_pathname: func.url_path(config.sys.base_route+config.sys.home_route),
                url_params: func.get_params(),
            });
        }
    };


    // 页面函数执行的入口，实时更新数据
    function page_start(){
        func.console_log("page_start=", route);
        // 开始
        // 兼容老View框架的路由
        if (href.indexOf("route=home") != -1){
            let array = href.split("route=home");
            let url = "";
            if (array.length >= 2){
                url = host + config.sys.home_route + "?" + array[1];
            }else{
                url = host + config.sys.home_route + "";
            }
            // 处理url格式
            url = url.replaceAll("//", "/");
            if (url.indexOf("/") === 0){
                url = url.replace("/", "");
            }
            url = "//"+url;
            //
            func.open_url(url);
        }
        else if (href.indexOf("route=search") != -1){
            let array = href.split("route=search");
            let url = "";
            if (array.length >= 2){
                url = host + "search?" + array[1];
            }else{
                url = host + "search";
            }
            func.open_url(url);
        }
        else if (href.indexOf("route=info") != -1){
            let array = href.split("route=info");
            let url = "";
            if (array.length >= 2){
                url = host + "info?" + array[1];
            }else{
                url = host + "info"
            }
            func.open_url(url);
        }
        // 新版直接跳转
        else{
            def.go_home();
        }
    }

    // 标签处于切换显示状态
    function page_show(){
        func.console_log("page_show=", route);
        // show
    }

    // 标签处于切换隐藏状态
    function page_hide(){
        func.console_log("page_hide=", route);
        // hide
    }


    // 刷新页面数据
    afterNavigate(() => {
        if (!runtime_ok() || !browser_ok()){return;} // 系统基础条件检测
        // 开始
        page_start();
    });


    // 页面装载完成后，只运行一次
    // addEventListener专用函数
    onMount(() => {
        if (!runtime_ok() || !browser_ok()){return;} // 系统基础条件检测
        // 监测页面标签是否处于显示
        if (browser){
            document.addEventListener("visibilitychange", () => {
                if (document.hidden) { // onHide
                    page_show();
                } else { // onShow
                    page_hide();
                }
            });
        }
    });


</script>

<div class="page-div index-box select-none"></div>

<style>
    .index-box{
        padding: 10px 10px;
    }
</style>