<script lang="ts">
    import { resolve } from '$app/paths';
    import { page } from '$app/state';
    import func from "../../common/func.svelte.js";
    import {afterNavigate} from "$app/navigation";
    import {onMount} from "svelte";

    // 本页面参数
    let route = $state(func.get_route());


    // 本页面函数：Svelte的HTML组件onXXX=中正确调用：={()=>def.xxx()}
    const def = {
        //
    };


    // 检测$state()值变化
    $effect(() => {
        //
    });


    // 刷新页面数据
    afterNavigate(() => {
        //
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