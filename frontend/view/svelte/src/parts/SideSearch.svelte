<script lang="ts">
    import {afterNavigate} from "$app/navigation";
    import func from "../common/func.svelte.js";
    import {input_enter_data} from "../stores/input_enter.store.svelte";
    import {browser_ok, runtime_ok} from "../common/middleware.svelte";
    import config from "../config";
    import {browser} from "$app/environment";

    // 本页面参数
    let input_value_search = $state("");
    let input_object: any; // input标签dom对象


    // 本页面函数：Svelte的HTML组件onXXX=中正确调用：={()=>def.xxx()}
    const def = {
        input_run_search: function(){
            let that = this;
            // 执行回车操作
            // that.clear_input_value();
            let the_value = input_value_search.trim();
            if (the_value){
                if (the_value === config.sys.home_route_white_word){ // 必要，home页面
                    let href = "."+config.sys.home_route+"?cache="+func.js_rand(100000, 9999999)
                    href = href.replaceAll(".?cache=", "./?cache=");
                    href = href.replaceAll("//", "/");
                    that.open_url(href);
                }
                else if (the_value === "@reload" || the_value === "@fresh" || the_value === "@refresh"){
                    func.fresh_page(0);
                }
                else if (the_value === "@404"){
                    that.open_url("./_404");
                }
                else if (the_value === "@info"){
                    that.open_url("./info");
                }
                else{
                    func.notice("Enter: "+ the_value);
                }
            }else{
                func.notice(func.get_translate("input_null"));
            }
        },
        open_url: function(href=""){
            func.open_url(href, "_self");
        },
        clear_input_value: function(){
            setTimeout(function (){
                input_value_search = "";
            }, 500);
        },
        input_enter: function(event: any){
            let that = this;
            //
            if (event.key === 'Enter') {
                let that = this;
                // 处理Enter
                if (event.key === 'Enter') {
                    let the_value = input_value_search.trim();
                    if (input_enter_data.input_doing === 1 || input_enter_data.input_doing === 2){ // 输入法输入完成
                        console.log("输入法输入完成=", input_enter_data.input_doing, the_value);
                        input_enter_data.input_doing = -1; // init
                        that.input_run_search();
                    }else{ // 输入法正在输入
                        that.input_run_search();
                    }
                }
            }
        },
    };


    // 刷新页面数据
    afterNavigate(() => {
        if (!func.support_min_js()){return;}
        if (!runtime_ok() || !browser_ok()){return;} // 系统基础条件检测
        // 监听输入法输入事件
        func.watch_input_enter(input_object);
    });


</script>

<section class="section-side_search select-none bg-neutral-200 dark:bg-neutral-800">
    <div class="side-search font-text">
        <label class="label">
            <input class="side-search-input input-style w-full border-radius font-text select-text" type="search" maxlength="2000" placeholder="{func.get_translate('input_placeholder_search')}"
                   bind:value={input_value_search}
                   onkeydown={(event)=>def.input_enter(event)}
                   onmouseenter={(e) => e.currentTarget.focus()}
                   bind:this={input_object}
            />
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