<script lang="ts">
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

<section class="section-side_search select-none bg-neutral-200 dark:bg-neutral-800">
    <div class="side-search font-text">
        <label class="label">
            <input class="side-search-input input w-full border-radius font-text select-text" type="text" maxlength="1000" placeholder="Input..." />
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
    .side-search-input{
        height: 40px;
        display: block;
        background: rgba(200, 200, 200, 0.1);
    }

</style>