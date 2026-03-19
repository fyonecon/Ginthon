<script lang="ts">
    import { resolve } from '$app/paths';
    import func from "../../common/func.svelte.js";
    import config from "../../config";
    import {afterNavigate} from "$app/navigation";
    import {onMount} from "svelte";
    import {browser_ok, runtime_ok} from "../../common/middleware.svelte";
    import {browser} from "$app/environment";
    import FetchPOST from "../../common/post.svelte";
    import FetchGET from "../../common/get.svelte";


    // 本页面参数
    let route = $state(func.get_route());
    const loading_img = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"><path stroke-dasharray="16" stroke-dashoffset="16" d="M12 3c4.97 0 9 4.03 9 9"><animate fill="freeze" attributeName="stroke-dashoffset" dur="0.3s" values="16;0"/><animateTransform attributeName="transform" dur="1.5s" repeatCount="indefinite" type="rotate" values="0 12 12;360 12 12"/></path><path stroke-dasharray="64" stroke-dashoffset="64" stroke-opacity="0.3" d="M12 3c4.97 0 9 4.03 9 9c0 4.97 -4.03 9 -9 9c-4.97 0 -9 -4.03 -9 -9c0 -4.97 4.03 -9 9 -9Z"><animate fill="freeze" attributeName="stroke-dashoffset" dur="1.2s" values="64;0"/></path></g></svg>';
    let ping_google = $state("...");
    let ping_bing = $state("...");
    let ping_youtube = $state("...");
    let ping_ithome = $state("...");
    let ping_github = $state("...");
    let ping_host = $state("...");
    let ping_hosts = $state("...");
    let test_db_data = $state("...");
    let test_index_html_api = $state("...");
    let test_index_html_info: object[]  = $state([]);

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
            ping_github = loading_img;
            ping_host = loading_img;
            ping_hosts = loading_img;
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
            that.ping_url("https://www.github.com").then(msg => {
                ping_github = msg;
            });
            that.ping_url("http://"+func.get_host()).then(msg => {
                ping_host = msg;
            });
            that.ping_url("https://"+func.get_host()).then(msg => {
                ping_hosts = msg;
            });
        },
        see_ip_detail: function(){
            let see = "https://ip.im";
            let href = "./search?word="+encodeURIComponent(func.string_to_unicode(see))+"&engine=bing&url_timeout="+func.url_timeout_encode("search", 0.5*60*60)+"&ap=info";
            if (browser){
                if (func.is_wails() || func.is_gthon()){
                    func.open_url_with_default_browser(href);
                }else{
                    if (func.is_mobile_screen()){
                        window.open(href, "_self");
                    }else{
                        window.open(href, "_blank");
                    }
                }
            }else{
                func.open_url_with_default_browser(href);
            }
        },
        test_db: function(){
            let that = this;
            //
            test_db_data = "Loading...";
            let mark = func.get_time_date("Y-m-d H:i");
            func.set_db_data("test_" + mark, "This db data. " + mark).then(value=>{
                // console.log(value);
                test_db_data = value;
            });
        },
        test_index_html: function(){
            test_index_html_api = "//" + window.location.host;
            test_index_html_info = [{
                key: "File URL",
                value: test_index_html_api,
            }];
            fetch(test_index_html_api).then(response => {
                let headers = response.headers;
                let index = 0;
                for (let [key, value] of headers) {
                    // console.log(`${key}: ${value}`);
                    if (index < 5){ // 不需要展示全部
                        test_index_html_info.push({
                            key: key,
                            value: value,
                        });
                    }
                    ++index;
                }
            });
        },
    };


    // 页面函数执行的入口，实时更新数据
    function page_start(){
        func.console_log("page_start=", route);
        func.loading_hide(); // 避免其他页面跳转到本页面时出现loading图
        // 开始
        func.title(func.get_translate("Info"));
        def.test_index_html();
    }

    // 标签处于切换显示状态
    function page_show(){
        func.console_log("page_show=", route);
        // show
    }

    // 标签处于切换隐藏状态
    function page_hide(){
        func.console_log("page_hide=", route);
        // hide
    }


    // 刷新页面数据
    afterNavigate(() => {
        if (!func.support_min_js()){return;}
        if (!runtime_ok() || !browser_ok()){return;} // 系统基础条件检测
        //
        page_start();
    });


    // 页面装载完成后，只运行一次
    // addEventListener专用函数
    onMount(() => {
        if (!func.support_min_js()){return;}
        if (!runtime_ok() || !browser_ok()){return;} // 系统基础条件检测
        // 监测页面标签是否处于显示
        if (browser){
            document.addEventListener("visibilitychange", () => {
                if (document.hidden) { // onHide
                    page_show();
                } else { // onShow
                    page_hide();
                }
            });
        }
    });


</script>

<div class="page-div info-box select-none">

    <div class="info-div font-text">
        <div class="info-div-title">
            <span class="font-text">Ping 网络 </span>
            <button type="button" class="btn btn-sm preset-filled-primary-500 font-mini click" onclick={()=>def.ping_show()} title="Click">Start</button>
        </div>
        <div class="info-div-content">
            <div class="info-div-content-li break">
                <span class="info-div-content-li-title select-text float-left">google.com ：</span>
                <span class="info-div-content-li-res float-left">{@html ping_google}</span>
                <div class="clear"></div>
            </div>
            <div class="info-div-content-li break">
                <span class="info-div-content-li-title select-text float-left">bing.com ：</span>
                <span class="info-div-content-li-res float-left">{@html ping_bing}</span>
                <div class="clear"></div>
            </div>
            <div class="info-div-content-li break">
                <span class="info-div-content-li-title select-text float-left">youtube.com ：</span>
                <span class="info-div-content-li-res float-left">{@html ping_youtube}</span>
                <div class="clear"></div>
            </div>
            <div class="info-div-content-li break">
                <span class="info-div-content-li-title select-text float-left">ithome.com ：</span>
                <span class="info-div-content-li-res float-left">{@html ping_ithome}</span>
                <div class="clear"></div>
            </div>
            <div class="info-div-content-li break">
                <span class="info-div-content-li-title select-text float-left">github.com ：</span>
                <span class="info-div-content-li-res float-left">{@html ping_github}</span>
                <div class="clear"></div>
            </div>
            <div class="info-div-content-li break">
                <span class="info-div-content-li-title select-text float-left">http://{func.get_host()} ：</span>
                <span class="info-div-content-li-res float-left">{@html ping_host}</span>
                <div class="clear"></div>
            </div>
            <div class="info-div-content-li break">
                <span class="info-div-content-li-title select-text float-left">https://{func.get_host()} ：</span>
                <span class="info-div-content-li-res float-left">{@html ping_hosts}</span>
                <div class="clear"></div>
            </div>
        </div>
    </div>

    <div class="info-div font-text">
        <div class="info-div-title">
            <span class="font-text">用户 IP </span>
            <button type="button" class="btn btn-sm preset-filled-primary-500 font-mini click" onclick={()=>def.see_ip_detail()} title="Click">Detail</button>
        </div>
        <div class="info-div-content">
<!--            <img src="//ip.im/img" alt="My IP Address" style="min-width: 215px; height: 70px; width: 100%;">-->
            <span style="opacity: 0.6;">(点击上面 Detail 按钮可查看)</span>
        </div>
    </div>

    <div class="info-div font-text">
        <div class="info-div-title">
            <span class="font-text">浏览器信息</span>
        </div>
        <div class="info-div-content">
            <div class="info-div-content-li break select-text">
                <span class="info-div-content-li-title ">UserAgent ：</span>
                <br>
                <span class="info-div-content-li-res">{@html window.navigator.userAgent}</span>
                <div class="clear"></div>
            </div>
            <div class="info-div-content-li break select-text">
                <span class="info-div-content-li-title ">浏览器时区 ：</span>
                <br>
                <span class="info-div-content-li-res">{@html Intl.DateTimeFormat().resolvedOptions().timeZone || "-不支持-"}</span>
                <div class="clear"></div>
            </div>
            <div class="info-div-content-li break select-text">
                <span class="info-div-content-li-title ">浏览器语言 ：</span>
                <br>
                <span class="info-div-content-li-res">{@html window.navigator.languages}</span>
                <div class="clear"></div>
            </div>
            <div class="info-div-content-li break select-text">
                <span class="info-div-content-li-title ">设备CPU数(逻辑核) ：</span>
                <br>
                <span class="info-div-content-li-res">{@html window.navigator.hardwareConcurrency || "-不支持-"}</span>
                <div class="clear"></div>
            </div>
            <div class="info-div-content-li break select-text">
                <span class="info-div-content-li-title ">设备内存(GB) ：</span>
                <br>
                <span class="info-div-content-li-res">{@html window.navigator.deviceMemory || "-不支持-"}</span>
                <div class="clear"></div>
            </div>
            <div class="info-div-content-li break select-text">
                <span class="info-div-content-li-title ">Screen尺度参数 ：</span>
                <br>
                <span class="info-div-content-li-res">
                    {@html
                        "screen.width=" + window.screen.width+
                        "<br/>screen.height=" + window.screen.height+
                        "<br/>screen.availWidth=" + window.screen.availWidth+
                        "<br/>screen.availHeight=" + window.screen.availHeight
                    }
                </span>
                <div class="clear"></div>
            </div>
            <div class="info-div-content-li break select-text">
                <span class="info-div-content-li-title ">Pages尺度参数 ：</span>
                <br>
                <span class="info-div-content-li-res">{@html
                    "window.innerWidth=" + window.innerWidth +
                    "<br/>window.innerHeight=" + window.innerHeight
                }
                </span>
                <div class="clear"></div>
            </div>

            <div class="info-div-content-li break select-text">
                <span class="info-div-content-li-title ">是否处于PWA(Mobile、PC) ：</span>
                <br>
                <span class="info-div-content-li-res">{@html [func.is_mobile_pwa(), func.is_pc_pwa()]}</span>
                <div class="clear"></div>
            </div>
            <div class="info-div-content-li break select-text">
                <span class="info-div-content-li-title ">IsMobileScreen ：</span>
                <br>
                <span class="info-div-content-li-res">{@html func.is_mobile_screen()}</span>
                <div class="clear"></div>
            </div>
            <div class="info-div-content-li break select-text">
                <span class="info-div-content-li-title ">浏览器主题 ：</span>
                <br>
                <span class="info-div-content-li-res">{@html func.get_theme_model()}</span>
                <div class="clear"></div>
            </div>
            <div class="info-div-content-li break select-text">
                <span class="info-div-content-li-title ">当前地址的Refer ：</span>
                <br>
                <span class="info-div-content-li-res">{@html document.referrer.slice(0, 120)+ " ..."}</span>
                <div class="clear"></div>
            </div>
            <div class="info-div-content-li break select-text">
                <span class="info-div-content-li-title ">当前地址的Host ：</span>
                <br>
                <span class="info-div-content-li-res">{@html window.location.host}</span>
                <div class="clear"></div>
            </div>
            <div class="info-div-content-li break select-text">
                <span class="info-div-content-li-title ">appVersion ：</span>
                <br>
                <span class="info-div-content-li-res">{@html "v"+config.app.app_version}</span>
                <div class="clear"></div>
            </div>
            <div class="info-div-content-li break select-text">
                <span class="info-div-content-li-title ">appUID ：</span>
                <br>
                <span class="info-div-content-li-res">{@html "-"}</span>
                <div class="clear"></div>
            </div>
            <div class="info-div-content-li break select-text">
                <span class="info-div-content-li-title ">Date ：</span>
                <br>
                <span class="info-div-content-li-res">{@html func.get_time_date("Y/m/d")}</span>
                <div class="clear"></div>
            </div>
        </div>
    </div>

    <div class="info-div font-text">
        <div class="info-div-title">
            <span class="font-text">CDN 文件信息</span>
        </div>
        <div class="info-div-content ">
            {#each test_index_html_info as info}
                <div class="info-div-content-li break select-text">
                    <span class="info-div-content-li-title ">{@html info.key}:  </span>
                    <br>
                    <span class="info-div-content-li-res ">{@html info.value}</span>
                    <div class="clear"></div>
                </div>
            {/each}
        </div>
    </div>

</div>

<style>
    .info-box{
        padding: 10px 10px;
    }

    .info-div{
        border-radius: 10px;
        margin-bottom: 20px;
    }

    .info-div-title{
        padding: 10px 0;
        text-indent: 2px;
    }
    .info-div-content{
        padding: 10px 10px;
        border-radius: 10px;
        border: 1px solid rgba(160,160,160, 0.6);
    }

    .info-div-content-li{
        margin-bottom: 10px;
    }

    .info-div-content-li-title{
        line-height: 30px;
    }
    .info-div-content-li-res{
        line-height: 22px;
        opacity: 0.6;
    }

</style>