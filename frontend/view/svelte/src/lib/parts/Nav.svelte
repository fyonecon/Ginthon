<script>
    import { sideTabData } from '$lib/stores/side_tab_store.js';

    // 从 store 获取数据
    $: side_tab_data = $sideTabData;

</script>


<section class="section-nav pywebview-drag-region can-drag">

    <div class="nav-title-div center select-none font-title" data-nav_value="{side_tab_data.tab_value}">{side_tab_data.tab_name}</div>

</section>

<style>
    .nav-title-div{
        height: 50px;
        line-height: 50px;
        overflow: hidden;
        opacity: 0.8;
    }
</style>