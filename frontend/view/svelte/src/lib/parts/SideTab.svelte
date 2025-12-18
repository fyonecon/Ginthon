<script lang="ts">
    import { resolve } from '$app/paths';
    import { page } from '$app/state';
    import func from "$lib/common/func.svelte.js";
    import { afterNavigate, beforeNavigate } from "$app/navigation";
    import config from "$lib/config.js";
    import { side_tab_data } from '$lib/stores/side_tab.store.svelte.js';

    // 将路由转化为翻译的键
    function get_route_name(route="") {
        switch (route) {
            case "/home":
                return "Home";
            case "/_404":
                return "_404";
            case "/settings":
                return "Settings";
            case "/settings/about":
                return "About";
            default:
                return "";
        }
    }


    // 页面数据
    let route = $state(func.get_route());


    // 刷新页面数据
    afterNavigate(() => {
        route = func.get_route();
        //
        side_tab_data.tab_value = route;
        side_tab_data.tab_name = func.get_translate(get_route_name(route));
    });

</script>

<section class="section-side_tab select-none bg-neutral-100 dark:bg-neutral-800 border-radius">
    <ul class="side_tab-menu-ul scroll-y-style select-none font-text border-radius bg-neutral-100 dark:bg-neutral-800">
        <li class="side_tab-menu-li">
            <a class="side_tab-menu-a border-radius break {route==='/home'?' side_tab-menu-a-active ':' '} click" href={resolve(func.url_path('/home'))} ><svg class="svg-icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 20"><path fill="currentColor" fill-rule="evenodd" d="M2.52 7.823C2 8.77 2 9.915 2 12.203v1.522c0 3.9 0 5.851 1.172 7.063S6.229 22 10 22h4c3.771 0 5.657 0 6.828-1.212S22 17.626 22 13.725v-1.521c0-2.289 0-3.433-.52-4.381c-.518-.949-1.467-1.537-3.364-2.715l-2-1.241C14.111 2.622 13.108 2 12 2s-2.11.622-4.116 1.867l-2 1.241C3.987 6.286 3.038 6.874 2.519 7.823m6.927 7.575a.75.75 0 1 0-.894 1.204A5.77 5.77 0 0 0 12 17.75a5.77 5.77 0 0 0 3.447-1.148a.75.75 0 1 0-.894-1.204A4.27 4.27 0 0 1 12 16.25a4.27 4.27 0 0 1-2.553-.852" clip-rule="evenodd"/></svg>{func.get_translate("Home")}</a>
        </li>


    </ul>
</section>

<style>
    .section-side_tab {
        position: fixed;
        z-index: 0;
        width: 220px;
        padding: 0 10px 10px 10px;
        height: calc(100% - 100px - 40px);
        top: 100px;
        left: 0;
    }

    .side_tab-menu-ul{
        width: calc(100% - 8px);
        height: 100%;
        padding-bottom: 80px;
        position: absolute;
    }
    .side_tab-menu-li{
        width: 196px;
        max-height: calc(72px + 10px);
        overflow: hidden;
        clear: both;
    }
    .side_tab-menu-a{
        line-height: 24px;
        padding: 8px 8px;
        width: 100%;
        display: block;
        clear: both;
    }
    .side_tab-menu-a-active{
        background: rgba(200, 200, 200, 0.2);
        color: var(--color-blue-400);
    }

</style>