<script lang="ts">
	import SideTab from '../parts/SideTab.svelte';
	import Nav from '../parts/Nav.svelte';
	import Foot from '../parts/Foot.svelte';
	import './layout.css'; // 全局CSS

	/** @type {{children: import('svelte').Snippet}} */
	let { children } = $props();

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


    // 本页面参数
    let theme_model = $state(watch_theme_model_data.theme_model);


    // 本页面函数
    const def = {
        watch_404: function() { // 重定向到自定义的404页面
            let that = this;
            //
            if (page.status === 404) {
                func.redirect_pathname({
                    url_pathname: func.url_path("/_404"),
                    url_params: "?error_url=" + encodeURIComponent(func.get_href()) + "&error_msg=404 Route"
                });
            } else {
                let href = page.url.href;
                let host = page.url.host;
                let port = page.url.port;
                let route = page.route;
                let params = page.params;
                let search = page.url.search;
                let status = page.status;
                let origin = page.url.origin;
                let url_pathname = page.url.pathname;
                let url_param = page.url.searchParams;
                let app_uid = func.get_app_uid();

                func.console_log('当前页面参数=', {
                    href, host, port, route, params,
                    status, origin, url_pathname, url_param, search,
                    lang: navigator.language, langs: navigator.languages,
                    app_uid: app_uid,
                });
            }
        },
    };


	// 路由变化之前
	beforeNavigate(() => {
		//
	});

	// 路由变化之后
	afterNavigate(() => {
        def.watch_404(); // 检测路由变化
        theme_model = watch_theme_model_data.theme_model; // 检测主题变化
        //
	});

    // 监控所有变化
    $effect(() => {
        // console.log("layout=effect=", page.route);
    });

    // 页面装载完成后，只运行一次
    onMount(() => {
        func.js_watch_window_display(); // 监测窗口是否隐藏
        watch_window();
        //
    });

    //
    onDestroy(() => {
        //
    });

</script>

<div class="app bg-neutral-100 dark:bg-neutral-900" data-theme_model="{theme_model}">
    <SideLogo />
    <SideSearch />
	<SideTab />
    <SideSetting />
	<Nav />
    <Director />
	<main class="main">{@render children()}</main>
	<Foot />
    <PlayAudio />
    <!--  全局交互组件  -->
    <Loading />
    <Notice />
    <Alert />
</div>
