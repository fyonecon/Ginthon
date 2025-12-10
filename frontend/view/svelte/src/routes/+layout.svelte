<script>
    import Left from '$lib/parts/Left.svelte';
    import Nav from '$lib/parts/Nav.svelte';
    import Foot from '$lib/parts/Foot.svelte';
	import './layout.css';

	/** @type {{children: import('svelte').Snippet}} */
	let { children } = $props();

    import { onMount, onDestroy} from 'svelte';
    import { page } from '$app/state';
    import func from "$lib/common/func.js";
    import {afterNavigate, beforeNavigate} from "$app/navigation";
    import { browser, dev, building, version } from '$app/environment';

    // 重定向到自定义的404页面
    function watch_404(){
        if (page.status === 404) {
            func.redirect_pathname({
                url_pathname: func.url_path("/404"),
                url_param: "?error_url="+encodeURIComponent(func.get_href())+"&error_msg=404 Route",
            });
        }else{
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
            func.console_log('当前页面参数=', {
                href: href,
                host: host,
                port: port,
                route: route,
                params: params,
                status: status,
                origin: origin,
                url_pathname: url_pathname,
                url_param: url_param,
                search: search,
            });
        }
    }

    // 路由变化之前
    beforeNavigate(()=>{
        //
    });

    // 路由变化之后
    afterNavigate(()=>{
        watch_404();
    });

    // 页面装载完成后，只运行一次
    onMount(() => {
        func.console_log("onMount=", [browser, dev]);
        func.js_watch_window_display(); // 监测窗口是否隐藏

        // 其它
        // 展示主窗口
        func.js_call_py_or_go("window_show", {}).then(
            back_data=>{
                func.console_log("[视窗JS-Log]", "js_call_py.py返回值：", back_data);
            }
        );

    });

</script>

<div class="app">
    <Left />
    <Nav />

	<main class="main">
		{@render children()}
	</main>

	<Foot />
</div>