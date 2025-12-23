<script lang="ts">
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

<section class="section-side_search select-none bg-neutral-200 dark:bg-neutral-800">
    <div class="side-search font-text">
        <label class="label">
            <input class="side-search-input input-style w-full border-radius font-text select-text" type="text" maxlength="2000" placeholder="Input..." value="" />
        </label>
    </div>
</section>

<style>
    .section-side_search {
        position: fixed;
        z-index: 0;
        width: 220px;
        height: 42px;
        top: 50px;
        left: 0;
    }


    .side-search{
        height: 40px;
        padding: 0 2px;
    }

</style>