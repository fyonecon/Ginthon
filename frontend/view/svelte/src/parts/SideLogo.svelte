<script lang="ts">
    import config from "../config.js";
    import {afterNavigate} from "$app/navigation";
    import func from "../common/func.svelte";


    // 本页面参数
    let app_name = $state(config.app.app_name);
    let app_version = $state(config.app.app_version);

    // 本页面函数：Svelte的HTML组件onXXX=中正确调用：={()=>def.xxx()}
    const def = {
        //
    };


    // 刷新页面数据
    afterNavigate(() => {
        //
    });


</script>

<section class="section-side_logo scroll-y-style select-none pywebview-drag-region can-drag bg-neutral-200 dark:bg-neutral-800">
    <div class="side-logo center" ondblclick={()=>func.change_window_size()} role="button" tabindex="0">
        <span class="font-class hide">{app_name}</span>
        <span class="font-mini hide"> v{app_version}</span>
    </div>
</section>

<style>
    .section-side_logo {
        position: fixed;
        z-index: 0;
        width: 220px;
        height: 50px;
        top: 0;
        left: 0;
        overflow: hidden;
        padding: 5px 10px;
        border-top-right-radius: 10px;
        border-top-left-radius: 10px;
    }

    .side-logo{
        height: 40px;
        line-height: 40px;
        overflow: hidden;
        width: calc(100% - 0px);
        padding: 0 10px;
        cursor: default;
    }

</style>