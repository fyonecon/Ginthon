<script>
    import func from "../common/func.svelte.js";
    import {afterNavigate} from "$app/navigation";
    import {browser_ok, runtime_ok} from "../common/middleware.svelte.js";
    import config from "../config.js";


    // 本页面参数
    let route = $state(func.get_route());


    // 本页面函数：Svelte的HTML组件onXXX=中正确调用：={()=>def.xxx()}
    const def = {
        //
    };


    // 刷新页面数据
    afterNavigate(() => {
        if (!func.support_min_js()){return;}
        if (!runtime_ok() || !browser_ok()){return;} // 系统基础条件检测
        // 开始
        route = func.get_route();
    });


</script>

<div class="part-div Demo-box select-none">
    <div>{@html route}</div>
</div>

<style>
    .Demo-box{
        width: 100%;
    }

</style>