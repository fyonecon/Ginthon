<script lang="ts">
    import config from "../../config.js";

    // 页面数据
    let app_name = $state(config.app.app_name);
    let app_version = $state(config.app.app_version);


</script>

<section class="section-side_logo scroll-y-style select-none pywebview-drag-region can-drag bg-neutral-100 dark:bg-neutral-800">
    <div class="side-logo select-none center hide">
        <span class="font-class">{app_name}</span>
        <span class="font-mini"> v{app_version}</span>
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
    }

    .side-logo{
        height: 50px;
        line-height: 50px;
        overflow: hidden;
        width: calc(100%);
    }

</style>