<script lang="ts">
    import func from "..//common/func.svelte.js";
    import { page } from '$app/state';
    import { afterNavigate, beforeNavigate } from "$app/navigation";
    import config from "../config.js";
    import { side_tab_data } from '../stores/side_tab.store.svelte.js';


    // 本页面参数


    // 本页面函数：Svelte的HTML组件onXXX=中正确调用：={()=>def.xxx()}
    const def = {
        //
    };


    // 刷新页面数据
    afterNavigate(() => {
        //
    });


</script>


<section class="section-nav select-none pywebview-drag-region can-drag">
    <!--  标题  -->
    <div class="nav-title-div font-title font-bold" data-nav_value="{side_tab_data.tab_value}" ondblclick={()=>func.change_window_size()} role="button" tabindex="0">
        {side_tab_data.tab_name}
    </div>

</section>

<style>
    .section-nav {
        position: fixed;
        z-index: 0;
        width: calc(100% - 220px - 0px);
        min-width: 300px;
        height: 50px;
        top: 0;
        left: 220px;
        overflow-x: hidden;
        overflow-y: hidden;
    }
    .nav-title-div{
        height: 50px;
        line-height: 50px;
        overflow: hidden;
        padding-left: 10px;
        padding-right: 10px;
        opacity: 0.8;
        text-align: center;
        cursor: default;
    }
</style>