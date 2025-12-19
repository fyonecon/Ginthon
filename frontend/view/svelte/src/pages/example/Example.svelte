<script lang="ts">
    import { resolve } from '$app/paths';
    import { page } from '$app/state';
    import func from "../../common/func.svelte.js";
    import {afterNavigate} from "$app/navigation";
    import {onMount} from "svelte";

    // 本页面参数
    let route = $state(func.get_route());


    // 本页面函数
    const def = {
        //
    };


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
</div>