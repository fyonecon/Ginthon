<script lang="ts">
    import func from "../common/func.svelte";
    import config from "../config";
    import {afterNavigate} from "$app/navigation";


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

<section class="section-foot select-none pywebview-drag-region can-drag hide">
    <div class="center">Foot</div>
</section>

<style>
    .section-foot {
        position: fixed;
        z-index: 0;
        width: calc(100% - 220px);
        height: 20px;
        bottom: 0;
        right: 0;
        overflow-x: hidden;
        overflow-y: hidden;
    }
</style>