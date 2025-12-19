<script lang="ts">
    import func from "../common/func.svelte.js";
    import config from "../config.js";
    import {afterNavigate} from "$app/navigation";
    import {onMount} from "svelte";


    // 本页面参数


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

<section class="section-foot select-none  pywebview-drag-region can-drag bg-white dark:bg-neutral-900">
    <div class="center" style="opacity: 0.2; line-height: 40px;">
        {config.app.app_name}
    </div>
</section>

<style>
    .section-foot {
        position: fixed;
        z-index: 0;
        width: calc(100% - 220px);
        height: 40px;
        bottom: 0;
        right: 0;
        overflow-x: hidden;
        overflow-y: hidden;
    }
</style>