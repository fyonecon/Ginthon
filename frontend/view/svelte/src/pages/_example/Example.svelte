<script lang="ts">
    import { resolve } from '$app/paths';
    import func from "../../common/func.svelte.js";
    import {afterNavigate} from "$app/navigation";
    import {onMount} from "svelte";
    import {browser_ok, runtime_ok} from "../../common/middleware.svelte";

    
    // 本页面参数
    let route = $state(func.get_route());


    // 本页面函数：Svelte的HTML组件onXXX=中正确调用：={()=>def.xxx()}
    const def = {
        //
    };


    // 页面函数执行的入口，实时更新数据
    function page_start(){
        func.console_log("page_start()=", route);
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

<div>
    <h3>{route}</h3>
    <ul class="ul-group font-text">
        <li class="li-group">
            <div class="li-group-title break">
                test
            </div>
            <div class="li-group-content select-text">
                123
            </div>
        </li>

    </ul>
</div>