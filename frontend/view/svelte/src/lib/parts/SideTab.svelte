<script>
    import { resolve } from '$app/paths';
    import { page } from '$app/state';
    import func from "$lib/common/func.js";
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
    let app_name = $state(config.app.app_name);
    let app_version = $state(config.app.app_version);


    // 刷新页面数据
    afterNavigate(() => {
        route = func.get_route();
        //
        side_tab_data.tab_value = route;
        side_tab_data.tab_name = func.get_translate(get_route_name(route));
    });

</script>

<section class="section-side_tab scroll-y-style select-none">
    <div class="side_tab-logo select-none pywebview-drag-region can-drag center">
        <span class="font-class">{app_name}</span>
        <span class="font-mini"> v{app_version}</span>
    </div>
    <div class="side_tab-search font-text select-text">
        <label class="label">
            <input class="side_tab-search-input input w-full border-radius font-text" type="text" maxlength="1000" placeholder="Input..." />
        </label>
    </div>
    <ul class="side_tab-menu scroll-y-style select-none font-text">
        <li class="side_tab-menu-li">
            <a class="side_tab-menu-a border-radius break {route==='/home'?' side_tab-menu-a-active ':' '} click" href={resolve(func.url_path('/home'))}><svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 20"><path fill="currentColor" fill-rule="evenodd" d="M2.52 7.823C2 8.77 2 9.915 2 12.203v1.522c0 3.9 0 5.851 1.172 7.063S6.229 22 10 22h4c3.771 0 5.657 0 6.828-1.212S22 17.626 22 13.725v-1.521c0-2.289 0-3.433-.52-4.381c-.518-.949-1.467-1.537-3.364-2.715l-2-1.241C14.111 2.622 13.108 2 12 2s-2.11.622-4.116 1.867l-2 1.241C3.987 6.286 3.038 6.874 2.519 7.823m6.927 7.575a.75.75 0 1 0-.894 1.204A5.77 5.77 0 0 0 12 17.75a5.77 5.77 0 0 0 3.447-1.148a.75.75 0 1 0-.894-1.204A4.27 4.27 0 0 1 12 16.25a4.27 4.27 0 0 1-2.553-.852" clip-rule="evenodd"/></svg>{func.get_translate("Home")}</a>
        </li>
        <li class="side_tab-menu-li hide">
            <a class="side_tab-menu-a border-radius break {route==='/settings'?' side_tab-menu-a-active ':' '} click" href={resolve(func.url_path('/settings'))}><svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 20"><path fill="currentColor" fill-rule="evenodd" d="M14.279 2.152C13.909 2 13.439 2 12.5 2s-1.408 0-1.779.152a2 2 0 0 0-1.09 1.083c-.094.223-.13.484-.145.863a1.62 1.62 0 0 1-.796 1.353a1.64 1.64 0 0 1-1.579.008c-.338-.178-.583-.276-.825-.308a2.03 2.03 0 0 0-1.49.396c-.318.242-.553.646-1.022 1.453c-.47.807-.704 1.21-.757 1.605c-.07.526.074 1.058.4 1.479c.148.192.357.353.68.555c.477.297.783.803.783 1.361s-.306 1.064-.782 1.36c-.324.203-.533.364-.682.556a2 2 0 0 0-.399 1.479c.053.394.287.798.757 1.605s.704 1.21 1.022 1.453c.424.323.96.465 1.49.396c.242-.032.487-.13.825-.308a1.64 1.64 0 0 1 1.58.008c.486.28.774.795.795 1.353c.015.38.051.64.145.863c.204.49.596.88 1.09 1.083c.37.152.84.152 1.779.152s1.409 0 1.779-.152a2 2 0 0 0 1.09-1.083c.094-.223.13-.483.145-.863c.02-.558.309-1.074.796-1.353a1.64 1.64 0 0 1 1.579-.008c.338.178.583.276.825.308c.53.07 1.066-.073 1.49-.396c.318-.242.553-.646 1.022-1.453c.47-.807.704-1.21.757-1.605a2 2 0 0 0-.4-1.479c-.148-.192-.357-.353-.68-.555c-.477-.297-.783-.803-.783-1.361s.306-1.064.782-1.36c.324-.203.533-.364.682-.556a2 2 0 0 0 .399-1.479c-.053-.394-.287-.798-.757-1.605s-.704-1.21-1.022-1.453a2.03 2.03 0 0 0-1.49-.396c-.242.032-.487.13-.825.308a1.64 1.64 0 0 1-1.58-.008a1.62 1.62 0 0 1-.795-1.353c-.015-.38-.051-.64-.145-.863a2 2 0 0 0-1.09-1.083M12.5 15c1.67 0 3.023-1.343 3.023-3S14.169 9 12.5 9s-3.023 1.343-3.023 3s1.354 3 3.023 3" clip-rule="evenodd"/></svg>{func.get_translate("Settings")}</a>
        </li>
        <li class="side_tab-menu-li hide">
            <a class="side_tab-menu-a border-radius break {route==='/settings/about'?' side_tab-menu-a-active ':' '} click" href={resolve(func.url_path('/settings/about'))}><svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 20"><path fill="currentColor" fill-rule="evenodd" d="M12 22c-4.714 0-7.071 0-8.536-1.465C2 19.072 2 16.714 2 12s0-7.071 1.464-8.536C4.93 2 7.286 2 12 2s7.071 0 8.535 1.464C22 4.93 22 7.286 22 12s0 7.071-1.465 8.535C19.072 22 16.714 22 12 22m0-4.25a.75.75 0 0 0 .75-.75v-6a.75.75 0 0 0-1.5 0v6c0 .414.336.75.75.75M12 7a1 1 0 1 1 0 2a1 1 0 0 1 0-2" clip-rule="evenodd"/></svg>{func.get_translate("About")}</a>
        </li>
    </ul>
    <ul class="side_tab-footer select-none font-text">
        <li class="side_tab-menu-li">
            <a class="side_tab-menu-a border-radius break {route==='/settings'?' side_tab-menu-a-active ':' '} click" href={resolve(func.url_path('/settings'))}><svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 20"><path fill="currentColor" fill-rule="evenodd" d="M14.279 2.152C13.909 2 13.439 2 12.5 2s-1.408 0-1.779.152a2 2 0 0 0-1.09 1.083c-.094.223-.13.484-.145.863a1.62 1.62 0 0 1-.796 1.353a1.64 1.64 0 0 1-1.579.008c-.338-.178-.583-.276-.825-.308a2.03 2.03 0 0 0-1.49.396c-.318.242-.553.646-1.022 1.453c-.47.807-.704 1.21-.757 1.605c-.07.526.074 1.058.4 1.479c.148.192.357.353.68.555c.477.297.783.803.783 1.361s-.306 1.064-.782 1.36c-.324.203-.533.364-.682.556a2 2 0 0 0-.399 1.479c.053.394.287.798.757 1.605s.704 1.21 1.022 1.453c.424.323.96.465 1.49.396c.242-.032.487-.13.825-.308a1.64 1.64 0 0 1 1.58.008c.486.28.774.795.795 1.353c.015.38.051.64.145.863c.204.49.596.88 1.09 1.083c.37.152.84.152 1.779.152s1.409 0 1.779-.152a2 2 0 0 0 1.09-1.083c.094-.223.13-.483.145-.863c.02-.558.309-1.074.796-1.353a1.64 1.64 0 0 1 1.579-.008c.338.178.583.276.825.308c.53.07 1.066-.073 1.49-.396c.318-.242.553-.646 1.022-1.453c.47-.807.704-1.21.757-1.605a2 2 0 0 0-.4-1.479c-.148-.192-.357-.353-.68-.555c-.477-.297-.783-.803-.783-1.361s.306-1.064.782-1.36c.324-.203.533-.364.682-.556a2 2 0 0 0 .399-1.479c-.053-.394-.287-.798-.757-1.605s-.704-1.21-1.022-1.453a2.03 2.03 0 0 0-1.49-.396c-.242.032-.487.13-.825.308a1.64 1.64 0 0 1-1.58-.008a1.62 1.62 0 0 1-.795-1.353c-.015-.38-.051-.64-.145-.863a2 2 0 0 0-1.09-1.083M12.5 15c1.67 0 3.023-1.343 3.023-3S14.169 9 12.5 9s-3.023 1.343-3.023 3s1.354 3 3.023 3" clip-rule="evenodd"/></svg>{func.get_translate("Settings")}</a>
        </li>
    </ul>
</section>

<style>
    .side_tab-logo{
        height: 50px;
        line-height: 50px;
        overflow: hidden;
        width: calc(100%);
    }
    .side_tab-search{
        height: 50px;
        width: calc(100%);
    }
    .side_tab-search-input{
        height: 40px;
        display: block;
        background: rgba(200, 200, 200, 0.1);
    }
    .side_tab-menu{
        width: calc(100%);
    }
    .side_tab-menu-li{
        width: calc(100%);
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
    /*.side_tab-menu-a > svg{*/
    /*    float: left;*/
    /*    margin-right: 5px;*/
    /*}*/
    .side_tab-menu-a-active{
        background: rgba(200, 200, 200, 0.2);
        color: deepskyblue;
    }

    .side_tab-footer{
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
    }

</style>