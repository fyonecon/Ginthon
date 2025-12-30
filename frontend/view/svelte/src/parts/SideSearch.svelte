<script lang="ts">
    import {afterNavigate} from "$app/navigation";
    import func from "../common/func.svelte.js";

    // 本页面参数
    let input_value_search = $state("");


    // 本页面函数：Svelte的HTML组件onXXX=中正确调用：={()=>def.xxx()}
    const def = {
        input_enter: function(event){
            let that = this;
            //
            if (event.key === 'Enter') {
                console.log('Enter pressed:', input_value_search);
                // 执行回车操作
                let the_value = input_value_search.trim();
                if (the_value){
                    //
                    func.notice("Enter: "+ the_value);
                }else{
                    func.notice(func.get_translate("input_null"));
                }
            }
        },
    };


    // 刷新页面数据
    afterNavigate(() => {
        //
    });


</script>

<section class="section-side_search select-none bg-neutral-200 dark:bg-neutral-800">
    <div class="side-search font-text">
        <label class="label">
            <input class="side-search-input input-style w-full border-radius font-text select-text" type="text" maxlength="2000" placeholder="{func.get_translate('input_placeholder_search')}" bind:value={input_value_search} onkeydown={(event)=>def.input_enter(event)} onmouseenter={(e) => e.currentTarget.focus()} />
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
        width: 206px;
        margin-right: auto;
        margin-left: auto;
    }

</style>