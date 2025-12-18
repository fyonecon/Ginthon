<script lang="ts">
	import SideTab from '$lib/parts/SideTab.svelte';
	import Nav from '$lib/parts/Nav.svelte';
	import Foot from '$lib/parts/Foot.svelte';
	import './layout.css';

	/** @type {{children: import('svelte').Snippet}} */
	let { children } = $props();

	import { onMount, onDestroy } from 'svelte';
	import { page } from '$app/state';
	import func from "$lib/common/func.svelte.js";
	import { afterNavigate, beforeNavigate } from "$app/navigation";
    import SideLogo from "$lib/parts/SideLogo.svelte";
    import SideSearch from "$lib/parts/SideSearch.svelte";
    import SideFoot from "$lib/parts/SideFoot.svelte";
    import {watch_theme_model_data} from "$lib/stores/watch_theme_model.store.svelte.js";

	// 重定向到自定义的404页面
	function watch_404() {
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
				href,
				host,
				port,
				route,
				params,
				status,
				origin,
				url_pathname,
				url_param,
				search,
				lang: navigator.language,
				langs: navigator.languages,
                app_uid: app_uid,
			});
		}
	}

	// 兼容客户端
	// 写入系统必要数据
	function watch_window_runtime() {
		if (func.is_gthon()) {
			try {
				// 展示主窗口
				func.js_call_py_or_go("window_show", {}).then((back_data) => {
					func.console_log("[视窗JS-Log]", "js_call_py.py返回值：", back_data);
				});
			} catch(e) {
				console.error("不能导入gthon-UI相关文件");
			}
		} else if (func.is_wails()) {
			// try {
			//     import {Events} from "@wailsio/runtime";
			//     import {AppServicesForWindow} from "../../bindings/datathink.top/Waigo/internal/bootstrap";
			//     import config from "$lib/config.js";
			//
			//     // GoRunJS写入token，用于验证js_call_go
			//     Events.On("make_window_token", (result) => {
			//         const info = func.string_to_json(result.data);
			//         const app_class = config.app.app_class;
			//         // 设置新的
			//         const window_token = info.content["windowToken"];
			//         const window_token_timer = func.get_time_s_date("YmdHis");
			//         func.set_local_data(app_class+"window_token", window_token)
			//         func.set_local_data(app_class+"window_token_timer", window_token_timer)
			//         //
			//         const key = "stop_go_run_js_for_make_window_token";
			//         const data_dict = {};
			//         func.js_call_py_or_go(key, data_dict).then(res=>{
			//             if (res.state === 1){ // 成功
			//                 console.log("[func.js_call_go]",res);
			//             }else{
			//                 console.log(res.msg)
			//             }
			//         });
			//     });
			//
			//     //
			//     AppServicesForWindow.JSCallGo("test", {"data1": 2}).then(res=>{
			//         console.log(res);
			//     })
			//     AppServicesForWindow.Test().then(res=>{
			//         console.log(res);
			//     })
			// }catch (e) {
			//     console.error("不能导入Wails-UI相关文件");
			// }
		} else {
			console.warn("请指明Web运行的浏览器环境，否则数据不能初始化，只能使用简易Web功能。");
		}
	}

    // 页面数据
    let theme_model = $state(watch_theme_model_data.theme_model);

	// 路由变化之前
	beforeNavigate(() => {
		//
	});

	// 路由变化之后
	afterNavigate(() => {
		watch_404(); // 检测路由变化
        theme_model = watch_theme_model_data.theme_model; // 检测主题变化
        //
	});

	// 页面装载完成后，只运行一次
	onMount(() => {
		func.js_watch_window_display(); // 监测窗口是否隐藏
		watch_window_runtime();
        //
	});

    // 监控所有变化
    $effect(() => {
        // console.log("layout=effect=", page.route);
    });

</script>

<div class="app">
    <SideLogo />
    <SideSearch />
	<SideTab />
    <SideFoot />
	<Nav />
	<main class="main">{@render children()}</main>
	<Foot />
</div>
