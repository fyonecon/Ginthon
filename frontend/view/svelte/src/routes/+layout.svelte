<script lang="ts">
	import './layout.css'; // 全局CSS
	import { onMount, onDestroy } from 'svelte';
	import { page } from '$app/state';
	import func from "../common/func.svelte.js";
	import { afterNavigate, beforeNavigate } from "$app/navigation";
    import SideLogo from "../parts/SideLogo.svelte";
    import SideSearch from "../parts/SideSearch.svelte";
    import SideSetting from "../parts/SideSetting.svelte";
    import {watch_theme_model_data} from "../stores/watch_theme_model.store.svelte.js";
    import Director from "../parts/Director.svelte";
    import PlayAudio from "../parts/PlayAudio.svelte";
    import Loading from "../parts/Loading.svelte";
    import Notice from "../parts/Notice.svelte";
    import Alert from "../parts/Alert.svelte";
    import {watch_window} from "../watch_window.js";
    import {watch_lang_data} from "../stores/watch_lang.store.svelte.js";
    import config from "../config";
    import {app_uid_data} from "../stores/app_uid.store.svelte.js";
    import SideTab from '../parts/SideTab.svelte';
    import Nav from '../parts/Nav.svelte';
    import Foot from '../parts/Foot.svelte';
    import {runtime_ok} from "../common/runtime_ok.svelte.js";
    import {runtime_ok_data} from "../stores/runtime_ok.store.svelte.js";


    /** @type {{children: import('svelte').Snippet}} */
    let { children } = $props();


    // 本页面参数
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
            func.js_call_py_or_go("get_data", {data_key:lang_key}).then(res=>{
                let lang = res.content.data?res.content.data:func.get_lang();
                watch_lang_data.lang_index = lang;
                lang_index = lang; // 监测本地语言
            });
        },
        auto_set_theme_model: function () { // 自动切换主题
            const theme_model_key = config.app.app_class+"theme_model";
            func.js_call_py_or_go("get_data", {data_key:theme_model_key}).then(res=>{
                let mode=res.content.data;
                if (!mode) {
                    mode = func.get_theme_model();
                }
                watch_theme_model_data.theme_model = mode;
                theme_model = mode;
                document.documentElement.setAttribute('data-mode', mode);
            });
        }
    };


    // 监控所有$state()值变化
    $effect(() => {
        // console.log("layout=effect=", page.route);
    });


	// 路由变化之前
	beforeNavigate(() => {
		//
        runtime_ok_data.state = 0; // init
	});


	// 路由变化之后
	afterNavigate(() => {
        // 必要运行
        def.auto_set_language_index();
        def.auto_set_theme_model();
        // 系统基础条件检测
        if (!runtime_ok()){ // false
            func.alert_msg(func.get_translate("runtime_error_alert"), "long");
            page_display="hide";
            runtime_ok_data.state = -1;
            //
            return
        }else{ // 附加条件检测
            if (func.is_weixin() || func.is_work_weixin() || func.is_qq() || func.is_feishu() || func.is_dingding()){ // false
                func.alert_msg(func.get_translate("runtime_cn_chat_alert"), "long");
                page_display="hide";
                runtime_ok_data.state = -2;
                //
                return
            }else{ // ok
                runtime_ok_data.state = 1;
                page_display="show";
                //
                def.watch_404_route(); // 检测路由变化
            }
        }
	});


    // 页面装载完成后，只运行一次
    onMount(() => {
        if (!runtime_ok()){return;} // 系统基础条件检测
        //
        func.js_watch_window_display(); // 监测窗口是否隐藏
        watch_window();
        //
        func.get_app_uid().then(_app_uid=>{ // 设置app_uid
            app_uid_data.app_uid = _app_uid;
        });
        //
        let theme_event = window.matchMedia('(prefers-color-scheme: dark)');
        theme_event.addEventListener('change', function (event){ // 监测主题变化
            def.auto_set_theme_model();
        });
        //
    });


    //
    onDestroy(() => {
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