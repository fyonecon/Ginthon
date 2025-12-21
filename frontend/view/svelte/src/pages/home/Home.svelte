<script lang="ts">
    import { resolve } from '$app/paths';
    import { page } from '$app/state';
    import func from "../../common/func.svelte.js";
    import {afterNavigate} from "$app/navigation";
    import {onMount} from "svelte";
    import {Dialog, Portal} from "@skeletonlabs/skeleton-svelte";


    // 本页面参数
    let route = $state(func.get_route());
    const loading_img = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"><path stroke-dasharray="16" stroke-dashoffset="16" d="M12 3c4.97 0 9 4.03 9 9"><animate fill="freeze" attributeName="stroke-dashoffset" dur="0.3s" values="16;0"/><animateTransform attributeName="transform" dur="1.5s" repeatCount="indefinite" type="rotate" values="0 12 12;360 12 12"/></path><path stroke-dasharray="64" stroke-dashoffset="64" stroke-opacity="0.3" d="M12 3c4.97 0 9 4.03 9 9c0 4.97 -4.03 9 -9 9c-4.97 0 -9 -4.03 -9 -9c0 -4.97 4.03 -9 9 -9Z"><animate fill="freeze" attributeName="stroke-dashoffset" dur="1.2s" values="64;0"/></path></g></svg>';
    let ping_google = $state("...");
    let ping_bing = $state("...");
    let ping_youtube = $state("...");
    let ping_ithome = $state("...");
    let ping_host = $state("...");
    let test_db_data = $state("...");

    // 本页面函数：Svelte的HTML组件onXXX=中正确调用：={()=>def.xxx()}
    const def = {
        ping_url: function(url: string) {
            return new Promise((resolve) => {
                func.ping(url).then(back => {
                    console.log(url, back);
                    if (back.state === 1){
                        resolve(" ✅ ");
                    }else{
                        resolve(" ❌ ");
                    }
                });
            });
        },
        ping_show: function(){
            let that = this;
            console.log("ping_show=", that);
            //
            ping_google = loading_img;
            ping_bing = loading_img;
            ping_youtube = loading_img;
            ping_ithome = loading_img;
            ping_host = loading_img;
            //
            that.ping_url("https://www.google.com").then(msg => {
                ping_google = msg;
            });
            that.ping_url("https://www.bing.com").then(msg => {
                ping_bing = msg;
            });
            that.ping_url("https://www.youtube.com").then(msg => {
                ping_youtube = msg;
            });
            that.ping_url("https://www.ithome.com").then(msg => {
                ping_ithome = msg;
            });
            that.ping_url("http://"+func.get_host()).then(msg => {
                ping_host = msg;
            });
        },
        test_db: function(){
            let that = this;
            //
            test_db_data = "Loading...";
            let mark = func.get_time_date("Y-m-d H:i");
            func.set_db_data("test_" + mark, "This db data. " + mark).then(value=>{
                console.log(value);
                test_db_data = value;
            });
        },
    };


    // 刷新页面数据
    afterNavigate(() => {
        //
    });


    // 页面装载完成后，只运行一次
    onMount(() => {
        //
        // def.ping_show();
    });


</script>

<div>
    <ul class="ul-group font-text">
        <li class="li-group select-none">
            <div class="li-group-title break">
                Ping Network <button type="button" class="btn btn-sm preset-filled-primary-500" onclick={()=>def.ping_show()} title="Click">Start</button>
            </div>
            <div class="li-group-content">
                <div style="height: 5px;"></div>
                <p class="li-ping-p break">
                    <span class="ping-url">https://www.google.com</span>
                    <span class="ping-res">{@html ping_google}</span>
                </p>
                <p class="li-ping-p break">
                    <span class="ping-url">https://www.bing.com</span>
                    <span class="ping-res">{@html ping_bing}</span>
                </p>
                <p class="li-ping-p break">
                    <span class="ping-url">https://www.youtube.com</span>
                    <span class="ping-res">{@html ping_youtube}</span>
                </p>
                <p class="li-ping-p break">
                    <span class="ping-url">https://www.ithome.com</span>
                    <span class="ping-res">{@html ping_ithome}</span>
                </p>
                <p class="li-ping-p break">
                    <span class="ping-url">http://{func.get_host()}</span>
                    <span class="ping-res">{@html ping_host}</span>
                </p>
            </div>
        </li>
        <li class="li-group select-none">
            <div class="li-group-title break">
                indexDB <button type="button" class="btn btn-sm preset-filled-primary-500" onclick={()=>def.test_db()} title="Click">Start</button>
            </div>
            <div class="li-group-content">
                <p>{test_db_data}</p>
            </div>
        </li>

    </ul>
</div>

<style>
    .li-ping-p{
        clear: both;
        margin-bottom: 20px;
        padding-bottom: 20px;
    }
    .ping-url{
        float: left;
        margin-right: 10px;
        opacity: 0.8;
    }
    .ping-res{
        float: left;
    }
</style>