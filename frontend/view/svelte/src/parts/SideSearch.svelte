<script lang="ts">


</script>

<section class="section-side_search select-none bg-neutral-100 dark:bg-neutral-800 border-radius">
    <div class="side-search font-text select-text">
        <label class="label">
            <input class="side-search-input input w-full border-radius font-text" type="text" maxlength="1000" placeholder="Input..." />
        </label>
    </div>
</section>

<style>
    .section-side_search {
        position: fixed;
        z-index: 0;
        width: 220px;
        height: 50px;
        top: 50px;
        left: 0;
    }


    .side-search{
        height: 50px;
        padding: 0 2px;
    }
    .side-search-input{
        height: 40px;
        display: block;
        background: rgba(200, 200, 200, 0.1);
    }

</style>