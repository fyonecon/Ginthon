<script lang="ts">
    import { resolve } from '$app/paths';
    import func from "../../common/func.svelte";
    import FetchPOST from "../../common/post.svelte";
    import config from "../../config";
    import {onMount} from "svelte";
    import {afterNavigate} from "$app/navigation";
    import {browser_ok, runtime_ok} from "../../common/middleware.svelte";


    // 本页面参数
    let route = $state(func.get_route());
    let loading_tip = $state("...");
    let news_array = $state([]);


    // 本页面函数：Svelte的HTML组件onXXX=中正确调用：={()=>def.xxx()}
    const def = {
        read_ithome: function(){
            let that = this;
            //
            loading_tip = "Loading..."
            //
            const _api_url = config.api.api_host+"/api/spider/ithome";
            const _app_token = func.get_local_data("app_token");
            const body_dict = {
                lang: func.get_lang(),
                app_token: _app_token,
                app_class: config.app.app_class
            };
            FetchPOST(_api_url, body_dict).then(result=>{
                let state = result.state;
                let msg = result.msg;
                if (state === 1){
                    let array = result.content.array;
                    let url = result.content.it_url;
                    //
                    loading_tip = msg + "：" + url;
                    news_array = array;
                }else{ //
                    loading_tip = msg;
                }
            });
        },
    };


    // 页面函数执行的入口，实时更新数据
    function page_start(){
        console.log("page_start()=", route);
        // 开始
    }


    // 检测$state()值变化
    $effect(() => {
        //
    });


    // 刷新页面数据
    afterNavigate(() => {
        if (!runtime_ok() || !browser_ok()){return;}
        //
        page_start();
    });


    // 页面装载完成后，只运行一次
    onMount(() => {
        //
    });


</script>

<div>

    <ul class="ul-group font-text">
        <li class="li-group">
            <div class="li-group-title break">
                爬IT之家首页 <button type="button" class="btn btn-sm preset-filled-primary-500" onclick={()=>def.read_ithome()} title="Click">Start</button>
            </div>
            <div class="li-group-content select-text">
                <div style="height: 5px;"></div>
                <div>{loading_tip}</div>
                <ul>
                    {#each news_array as news, index}
                        <li style="margin-top: 20px;">
                            <div data-news_index="{news['news_index']}">{index}</div>
                            <div>详情：<span class="font-blue">{news["news_href"]}</span></div>
                            <div>标题：{decodeURIComponent(news["news_title"])}</div>
                            <div>ID：{news["news_id"]}</div>
                            <div>发布时间：{news["news_time"]}</div>
                            <div>评论数：{news["comments_num"]}</div>
                        </li>
                    {/each}
                </ul>
            </div>

        </li>
    </ul>

</div>