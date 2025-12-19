<script lang="ts">
    import func from "../common/func.svelte.js";
    import config from "../config.js";
    import {afterNavigate} from "$app/navigation";


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

<section class="section-foot select-none  pywebview-drag-region can-drag ">
    <div class="center" style="opacity: 0.1;"></div>
</section>

<style>
    .section-foot {
        position: fixed;
        z-index: 0;
        width: calc(100% - 220px);
        height: 5px;
        bottom: 0;
        right: 0;
        overflow-x: hidden;
        overflow-y: hidden;
    }
</style>