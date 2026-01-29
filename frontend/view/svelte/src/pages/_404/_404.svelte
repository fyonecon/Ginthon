<script lang="ts">
    import { resolve } from '$app/paths';
    import func from "../../common/func.svelte";
    import config from "../../config";
    import {afterNavigate} from "$app/navigation";
    import {onMount} from "svelte";
    import {browser_ok, runtime_ok} from "../../common/middleware.svelte";


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
        console.log("page_start()=", route);
        // 开始
    }


    // 检测$state()值变化
    $effect(() => {
        //
    });


    // 刷新页面数据
    afterNavigate(() => {
        if (!runtime_ok() || !browser_ok()){return;} // 系统基础条件检测
        //
        page_start();
    });


    // 页面装载完成后，只运行一次
    onMount(() => {
        //
    });


</script>

<div class="select-text">
    <br/>
    <h2 class="break">{error_msg?error_msg:"404"}</h2>
    <br/>
    <p class="break">{error_url?"Error URL: "+error_url:""}</p>
    <br/>
    <br/>
    <div class="" style="display:flex; justify-content: center; align-items: center;">
        <div>
            <a class="click font-blue" href={resolve(back_url)} target="_self" title="Back Home"><svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="10"/><path stroke-linecap="round" stroke-linejoin="round" d="m15.5 9l-3 3l3 3m-4-6l-3 3l3 3"/></g></svg> {func.get_translate("a_click_tip_back_home")}</a>
        </div>
    </div>
</div>