<script lang="ts">
    import { resolve } from '$app/paths';
    import func from "../../../common/func.svelte";
    import config from "../../../config";
    import { afterNavigate} from "$app/navigation";
    import {watch_theme_model_data} from "../../../stores/watch_theme_model.store.svelte";
    import {onDestroy, onMount} from "svelte";
    import {watch_lang_data} from "../../../stores/watch_lang.store.svelte";
    import {browser_ok, runtime_ok} from "../../../common/middleware.svelte";
    import { copy } from 'svelte-copy';
    import {side_tab_data} from "../../../stores/side_tab.store.svelte";


    // 本页面数据
    let route = $state(func.get_route());
    let app_uid = $state("");
    let user_agent = $state(func.get_agent());
    let href = $state(func.get_href());
    let params = $state(func.get_params());
    let languages = $state(navigator.languages);
    let theme_model = $state("");
    let language_index = $state("");
    let app_info = $state(config.app.app_name + " UI v"+config.app.app_version);
    let local_data_path = $state("");
    let time_interval_num = $state("");
    let time_interval_num_timer = $state(0);
    let local_cache_path = $state("");


    // 本页面函数：Svelte的HTML组件onXXX=中正确调用：={()=>def.xxx()}
    const def = {
        get_local_path: function(){
            func.js_call_py_or_go("get_local_path", {}).then(res=>{
                console.log(res);
                if (res.state === 1){
                    local_data_path = res.content.local_data_path;
                    local_cache_path = res.content.local_cache_path;
                }else{
                    local_data_path = "-";
                }
            });
        },
        get_time_interval_num: function(){
            func.js_call_py_or_go("get_time_interval_num", {}).then(res=>{
                if (res.state === 1){
                    time_interval_num = res.content.time_interval_num;
                }else{
                    time_interval_num = "-";
                }
            });
        },
    };


    // 页面函数执行的入口，实时更新数据
    function page_start(){
        console.log("page_start()=", route);
        // 开始
        func.title(func.get_translate("About"));
        side_tab_data.tab_value = route;
        side_tab_data.tab_name = func.get_translate("About");
        //
        func.get_app_uid().then(_app_uid=>{
            app_uid = _app_uid;
        });
        theme_model = watch_theme_model_data.theme_model;
        language_index = watch_lang_data.lang_index;
        //
        def.get_local_path();
        clearInterval(time_interval_num_timer);
        time_interval_num_timer = setInterval(function (){
            def.get_time_interval_num();
        }, 3000);
        //
    }


    // 检测$state()值变化
    $effect(() => {
        //
    });


    // 刷新页面数据
    afterNavigate(() => {
        if (!func.support_min_js()){return;}
        if (!runtime_ok() || !browser_ok()){return;} // 系统基础条件检测
        //
        page_start();
    });


    // 页面装载完成后，只运行一次
    onMount(() => {
        if (!func.support_min_js()){return;}
        if (!runtime_ok() || !browser_ok()){return;} // 系统基础条件检测
        //
    });

    //
    // 处理页面切换或关闭时的事件，比如定时器
    onDestroy(()=>{
        clearInterval(time_interval_num_timer);
    });


</script>

<div class="page-div select-none settings-about-box">
    <ul class="ul-group font-text select-none">
        <li class="li-group">
            <div class="li-group-title break">
                {func.get_translate("About")}
            </div>
            <div class="li-group-content select-text"
                 use:copy={{
                        text: app_info?app_info:"",
                        onCopy: ({ text }) => {text?func.notice(func.get_translate("copied"), "", 2000):func.console_log("Copied null");},
                        onError: ({ error }) => {func.notice(func.get_translate("copied_error"), "", 2000);console.warn(error);}
                      }}
            >
                {app_info}
            </div>
        </li>
        <li class="li-group">
            <div class="li-group-title break">
                Framework
            </div>
            <div class="li-group-content break select-text">
                <button type="button" class="a-btn font-blue click" onclick={()=>func.open_url_with_default_browser("https://github.com/fyonecon/Ginthon?ap=app")}>Ginthon(Python)</button>
                <button type="button" class="a-btn font-blue click" onclick={()=>func.open_url_with_default_browser("https://github.com/fyonecon/Waigo?ap=app")}>Waigo(Golang)</button>
            </div>
        </li>
        <li class="li-group">
            <div class="li-group-title break">
                UI
            </div>
            <div class="li-group-content break select-text">
                <button title="Open" type="button" class="a-btn font-blue click" onclick={()=>func.open_url_with_default_browser("https://svelte.js.cn/docs/svelte/overview")}>SvelteKit</button>
                <button title="Open" type="button" class="a-btn font-blue click" onclick={()=>func.open_url_with_default_browser("https://www.skeleton.dev/docs/svelte/guides/mode")}>SkeletonUI</button>
                <button title="Open" type="button" class="a-btn font-blue click" onclick={()=>func.open_url_with_default_browser("https://www.tailwindcss.cn/docs/installation")}>Tailwind CSS</button>
                <button title="Open" type="button" class="a-btn font-blue click" onclick={()=>func.open_url_with_default_browser("https://icon-sets.iconify.design/solar/")}>Iconify SVG</button>
            </div>
        </li>
        <li class="li-group">
            <div class="li-group-title break">
                Local Data Dir
            </div>
            <div class="li-group-content break"
                 use:copy={{
                        text: local_data_path?func.base64_decode(local_data_path):"",
                        onCopy: ({ text }) => {text?func.notice(func.get_translate("copied"), "", 2000):func.console_log("Copied null");},
                        onError: ({ error }) => {func.notice(func.get_translate("copied_error"), "", 2000);console.warn(error);}
                      }}
            >
                {local_data_path?local_data_path:"-"}
            </div>
        </li>
        <li class="li-group">
            <div class="li-group-title break">
                Local Cache Dir
            </div>
            <div class="li-group-content break"
                 use:copy={{
                        text: local_cache_path?func.base64_decode(local_cache_path):"",
                        onCopy: ({ text }) => {text?func.notice(func.get_translate("copied"), "", 2000):func.console_log("Copied null");},
                        onError: ({ error }) => {func.notice(func.get_translate("copied_error"), "", 2000);console.warn(error);}
                      }}
            >
               {local_cache_path?local_cache_path:"-"}
            </div>
        </li>
        <li class="li-group">
            <div class="li-group-title break">
                Time Interval Num
            </div>
            <div class="li-group-content break select-text">
                {time_interval_num?time_interval_num:"-"}
            </div>
        </li>
        <li class="li-group">
            <div class="li-group-title break">
                App UID
            </div>
            <div class="li-group-content break select-text">
                {app_uid?app_uid:"-"}
            </div>
        </li>
        <li class="li-group">
            <div class="li-group-title break">
                User Agent
            </div>
            <div class="li-group-content break"
                 use:copy={{
                        text: user_agent?user_agent:"",
                        onCopy: ({ text }) => {text?func.notice(func.get_translate("copied"), "", 2000):func.console_log("Copied null");},
                        onError: ({ error }) => {func.notice(func.get_translate("copied_error"), "", 2000);console.warn(error);}
                      }}
            >
                {func.base64_encode(user_agent)}
            </div>
        </li>
        <li class="li-group">
            <div class="li-group-title break">
                Href
            </div>
            <div class="li-group-content break">
                {func.base64_encode(href)}
            </div>
        </li>
        <li class="li-group">
            <div class="li-group-title break">
                Params
            </div>
            <div class="li-group-content break">
                {params?params:"-"}
            </div>
        </li>
        <li class="li-group">
            <div class="li-group-title break">
                Route
            </div>
            <div class="li-group-content break">
                {route}
            </div>
        </li>
        <li class="li-group">
            <div class="li-group-title break">
                Languages
            </div>
            <div class="li-group-content break select-text">
                {languages}
            </div>
        </li>
        <li class="li-group">
            <div class="li-group-title break">
                Showing Language
            </div>
            <div class="li-group-content break select-text">
                {language_index}
            </div>
        </li>
        <li class="li-group">
            <div class="li-group-title break">
                Themes
            </div>
            <div class="li-group-content break">
                {theme_model}
            </div>
        </li>
    </ul>
</div>