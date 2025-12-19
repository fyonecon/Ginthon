<script lang="ts">
    import { resolve } from '$app/paths';
    import { page } from '$app/state';
    import func from "$lib/common/func.svelte.js";
    import FetchPOST from "$lib/common/post.svelte";
    import config from "../../../config";
    import {onMount} from "svelte";

    //
    let loading_tip = $state("Loading..");
    let news_array = $state([]);
    function read_ithome(){
        loading_tip = "Loading..."
        //
        const _api_url = "http://127.0.0.1:9750/api/spider/ithome";
        const _app_token = func.get_local_data("app_token");
        const body_dict = {
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
    }

    // 页面装载完成后，只运行一次
    onMount(() => {
        read_ithome();
    });

</script>

<div style="padding: 10px 10px;">

    <div>
        <button type="button" class="btn preset-tonal-warning" onclick={read_ithome}>Load Spider</button>
    </div>

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