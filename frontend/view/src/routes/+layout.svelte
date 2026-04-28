<script lang="ts">
	import './layout.css'; // 全局CSS
    import './pages.css'; // 自定义的pages公共CSS
	import { onMount, onDestroy } from 'svelte';
    import { resolve } from '$app/paths';
	import { page } from '$app/state';
	import func from "../common/func.svelte";
	import { afterNavigate, beforeNavigate } from "$app/navigation";
    import SideLogo from "../parts/SideLogo.svelte";
    import SideSearch from "../parts/SideSearch.svelte";
    import SideSetting from "../parts/SideSetting.svelte";
    import {watch_theme_model_data} from "../stores/watch_theme_model.store.svelte";
    import Director from "../parts/Director.svelte";
    import PlayAudio from "../parts/PlayAudio.svelte";
    import Loading from "../parts/Loading.svelte";
    import Notice from "../parts/Notice.svelte";
    import Alert from "../parts/Alert.svelte";
    import {watch_window} from "../watch_window.js";
    import {watch_lang_data} from "../stores/watch_lang.store.svelte";
    import config from "../config";
    import SideTab from '../parts/SideTab.svelte';
    import Nav from '../parts/Nav.svelte';
    import Foot from '../parts/Foot.svelte';
    import {browser_ok, runtime_ok} from "../services/middleware.svelte";
    import {browser} from "$app/environment";


    /** @type {{children: import('svelte').Snippet}} */
    let { children } = $props();


    // 本页面参数
    let route = $state(func.get_route());
    let page_display = $state("hide");
    let theme_model = $state("");
    let lang_index = $state("");


    // 本页面函数
    const def = {
        watch_404_route: function() { // 重定向到自定义的404页面
            if (page.status === 404) {
                func.redirect_pathname({
                    url_pathname: func.url_path("/_404"),
                    url_params: "?error_url=" + encodeURIComponent(func.get_href()) + "&error_msg=404 Route"
                });
            }
        },
        auto_set_language_index: function(){ // 自动设置语言
            const lang_key = config.app.app_class+"language_index";
            func.js_call_py_or_go("get_data", {data_key:lang_key}).then((res: any)=>{
                let lang = res.content.data?res.content.data:func.get_lang();
                watch_lang_data.lang_index = lang;
                lang_index = lang; // 监测本地语言
            });
        },
        auto_set_theme_model: function () { // 自动切换主题
            const theme_model_key = config.app.app_class+"theme_model";
            func.js_call_py_or_go("get_data", {data_key:theme_model_key}).then((res: any)=>{
                let mode=res.content.data;
                if (!mode) {mode = func.get_theme_model();}
                watch_theme_model_data.theme_model = mode;
                theme_model = mode;
                document.documentElement.setAttribute('data-mode', mode);
            });
        },
        auto_set_theme_color: function(){ // bg-neutral-100 dark:bg-neutral-900
            let mode = func.get_theme_model();
            if (mode==="light") { // light
                func.set_theme_color("#FCFCFC");
            }else{ // dark
                func.set_theme_color("#171717");
            }
        },
        //

    };


    // 页面函数执行的入口，实时更新数据
    function page_start(){
        func.console_log("page_start=", route);
        func.loading_hide(); // 避免其他页面跳转到本页面时出现loading图
        // 开始
        route = func.get_route();

        // 确保项目所有js可以运行
        if (!func.support_min_js()){
            func.alert_msg(func.get_translate("support_min_js_alert"), "long");
            func.title("🔴");
            page_display="hide";
            setTimeout(function (){
                func.block_all_script();
            }, 100);
            return;
        }

        // 确保项目所有js可以运行
        if (!func.support_min_js()){
            func.alert_msg(func.get_translate("support_min_js_alert"), "long");
            func.title("🔴");
            page_display="hide";
            setTimeout(function (){
                func.block_all_script();
            }, 100);
            return;
        }

        // 系统基础条件检测
        if (!runtime_ok()){ // false
            let screen_w = 0;
            let screen_h = 0;
            let avail_w = 0;
            let avail_h = 0;
            if (browser){
                screen_w = window.screen.width;
                screen_h = window.screen.height;
                avail_w = window.screen.availWidth;
                avail_h = window.screen.availHeight;
            }
            func.alert_msg(func.get_translate("runtime_error_alert") + " - [" + screen_w.toString() + "x" +  screen_h.toString() + "_"+ avail_w.toString() + "x" + avail_h.toString()+"]", "long");
            func.title("⚠️");
            page_display="hide";
            return
        }

        // app浏览器检测
        if (!browser_ok()){ // false
            func.alert_msg(func.get_translate("runtime_cn_chat_alert"), "long");
            func.title("😅");
            page_display="hide";
            return
        }

        // 检测通过时
        page_display="show";
        def.watch_404_route(); // 检测路由变化
        //

    }

    // 标签处于切换显示状态
    function page_show(e: any){
        func.console_log("page_show=", route);
        // show
    }

    // 标签处于切换隐藏状态
    function page_hide(e: any){
        func.console_log("page_hide=", route);
        // hide
    }


    // 监控所有$state()值变化
    $effect(() => {
        // console.log("layout=effect=", page.route);
    });


	// 路由变化之前
	beforeNavigate(() => {
        //
	});


	// 路由变化之后
	afterNavigate(() => {
        //
        page_start();
	});


    // 页面装载完成后，只运行一次
    onMount(() => {
        // 设置app_uid
        func.get_app_uid().then(_app_uid => {});

        // 设置语言和主题
        if (func.is_waigo() || func.is_ginthon()) { // app
            def.auto_set_language_index();
            def.auto_set_theme_model();
            def.auto_set_theme_color();
            //
            let theme_event = window.matchMedia('(prefers-color-scheme: dark)');
            theme_event.addEventListener('change', function (event){ // 监测主题变化
                def.auto_set_theme_model();
                def.auto_set_theme_color();
            });
        } else { // web
            // 网站翻译语言
            let lang = func.get_lang();
            watch_lang_data.lang_index = lang;
            lang_index = lang;

            // 监听亮暗主题
            def.auto_set_theme_color();
            //
            let mode = func.get_theme_model();
            watch_theme_model_data.theme_model = mode;
            theme_model = mode;
            document.documentElement.setAttribute('data-mode', mode);
            //
            let theme_event = window.matchMedia('(prefers-color-scheme: dark)');
            theme_event.addEventListener('change', function (event){ // 监测主题变化
                def.auto_set_theme_color();
                //
                let mode = func.get_theme_model();
                watch_theme_model_data.theme_model = mode;
                theme_model = mode;
                document.documentElement.setAttribute('data-mode', mode);
            });
        }

        //
        if (!func.support_min_js()){return;}
        if (!runtime_ok() || !browser_ok()){return;} // 系统基础条件检测

        // 监测页面标签是否处于显示
        if (browser){
            document.addEventListener("visibilitychange", (e) => {
                if (document.hidden) { // onHide
                    page_hide(e);
                } else { // onShow
                    page_show(e);
                }
            });
        }

        //
        func.js_watch_window_display(); // 监测窗口是否隐藏
        watch_window();

    });


    // 处理页面切换或关闭时的事件，比如定时器
    onDestroy(()=>{
        //
    });


</script>

<div class="app {page_display} select-none" data-theme_model="{theme_model}" data-language_index="{lang_index}">
    <!-- 内容 -->
    <SideLogo />
    <SideSearch />
	<SideTab />
    <SideSetting />
    <Director />
	<Nav />
	<main class="main {page_display} ">{@render children()}</main>
	<Foot />
    <PlayAudio />
</div>

<div class="alert select-none">
    <!--  全局交互组件  -->
    <Loading />
    <Notice />
    <Alert />
</div>