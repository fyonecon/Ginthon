<script lang="ts">
    import func from "..//common/func.svelte.js";
    import { page } from '$app/state';
    import { afterNavigate, beforeNavigate } from "$app/navigation";
    import config from "../config.js";
    import { side_tab_data } from '../stores/side_tab.store.svelte.js';


    // 本页面参数


    // 本页面函数
    const def = {
        //
    };


    // 刷新页面数据
    afterNavigate(() => {
        //
    });


</script>


<section class="section-nav bg-neutral-200 dark:bg-neutral-800  pywebview-drag-region can-drag">
    <!--  标题  -->
    <div class="nav-title-div center select-none font-title font-bold" data-nav_value="{side_tab_data.tab_value}">{side_tab_data.tab_name}</div>

</section>

<style>
    .section-nav {
        position: fixed;
        z-index: 0;
        width: calc(100% - 220px);
        height: 50px;
        top: 0;
        right: 0;
        overflow-x: hidden;
        overflow-y: hidden;
    }
    .nav-title-div{
        height: 50px;
        line-height: 50px;
        overflow: hidden;
        opacity: 0.8;
    }
</style>