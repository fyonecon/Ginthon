<script lang="ts">
    import config from "../config.js";
    import {afterNavigate} from "$app/navigation";


    // 本页面参数
    let app_name = $state(config.app.app_name);
    let app_version = $state(config.app.app_version);

    // 本页面函数
    const def = {
        //
    };


    // 刷新页面数据
    afterNavigate(() => {
        //
    });


</script>

<section class="section-side_logo scroll-y-style select-none pywebview-drag-region can-drag bg-neutral-200 dark:bg-neutral-800">
    <div class="side-logo select-none center">
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
    }

</style>