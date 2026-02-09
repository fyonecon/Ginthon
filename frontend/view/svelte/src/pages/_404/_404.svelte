<script lang="ts">
    import { resolve } from '$app/paths';
    import func from "../../common/func.svelte.js";
    import config from "../../config";
    import {afterNavigate} from "$app/navigation";
    import {onMount} from "svelte";
    import {browser_ok, runtime_ok} from "../../common/middleware.svelte";
    import {browser} from "$app/environment";


    // 链接携带的信息
    const error_url = func.search_param("error_url")
    const error_msg = func.search_param("error_msg");
    const back_url = func.url_path(config.sys.home_route);


    // 本页面参数
    let route = $state(func.get_route());


    // 本页面函数：Svelte的HTML组件onXXX=中正确调用：={()=>def.xxx()}
    const def = {
        //
    };


    // 页面函数执行的入口，实时更新数据
    function page_start(){
        func.console_log("page_start=", route);
        func.loading_hide(); // 避免其他页面跳转到本页面时出现loading图
        // 开始
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
        //
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

<div class="page-div _404-box select-none">
    <div class="select-text">
        <br/>
        <h2 class="break" data-error_msg="{error_msg}">{error_msg?error_msg:"404"}</h2>
        <br/>
        <p class="break" data-error_url="{error_url}">{error_url?"Error URL: "+error_url.slice(0, 120)+" ... ":""}</p>
        <br/>
        <br/>
        <div class="" style="display:flex; justify-content: center; align-items: center;">
            <div style="clear: both;">
                <a class="click font-blue" href={resolve(back_url)} target="_self" title="Back Home"><svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" style="float: left; margin-right: 10px;"><g fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="10"/><path stroke-linecap="round" stroke-linejoin="round" d="m15.5 9l-3 3l3 3m-4-6l-3 3l3 3"/></g></svg>{func.get_translate("a_click_tip_back_home")}</a>
            </div>
        </div>
        <br/>
        <br/>
        <br/>
        <br/>
    </div>
</div>

<style>
    ._404-box{
        padding: 20px 15px;
    }
</style>