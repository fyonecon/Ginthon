<script>
    import { resolve } from '$app/paths';
    import { page } from '$app/state';
    import func from "$lib/common/func.svelte.js";
    import { afterNavigate, beforeNavigate } from "$app/navigation";


    // 页面数据
    let route = $state(func.get_route());


    // 刷新页面数据
    afterNavigate(() => {
        route = func.get_route();
    });

</script>

<section class="section-side_foot select-none bg-neutral-100 dark:bg-neutral-800 border-radius">
    <!--    -->
    <ul class="side_foot-ul select-none font-text border-radius bg-neutral-100 dark:bg-neutral-800">
        <li class="side_foot-menu-li">
            <a class="side_foot-menu-a border-radius break {(route==='/settings' || route.indexOf('/settings/') === 0)?' side_foot-menu-a-active ':' '} click" href={resolve(func.url_path('/settings'))} ><svg  class="svg-icon"  xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 20"><path fill="currentColor" fill-rule="evenodd" d="M14.279 2.152C13.909 2 13.439 2 12.5 2s-1.408 0-1.779.152a2 2 0 0 0-1.09 1.083c-.094.223-.13.484-.145.863a1.62 1.62 0 0 1-.796 1.353a1.64 1.64 0 0 1-1.579.008c-.338-.178-.583-.276-.825-.308a2.03 2.03 0 0 0-1.49.396c-.318.242-.553.646-1.022 1.453c-.47.807-.704 1.21-.757 1.605c-.07.526.074 1.058.4 1.479c.148.192.357.353.68.555c.477.297.783.803.783 1.361s-.306 1.064-.782 1.36c-.324.203-.533.364-.682.556a2 2 0 0 0-.399 1.479c.053.394.287.798.757 1.605s.704 1.21 1.022 1.453c.424.323.96.465 1.49.396c.242-.032.487-.13.825-.308a1.64 1.64 0 0 1 1.58.008c.486.28.774.795.795 1.353c.015.38.051.64.145.863c.204.49.596.88 1.09 1.083c.37.152.84.152 1.779.152s1.409 0 1.779-.152a2 2 0 0 0 1.09-1.083c.094-.223.13-.483.145-.863c.02-.558.309-1.074.796-1.353a1.64 1.64 0 0 1 1.579-.008c.338.178.583.276.825.308c.53.07 1.066-.073 1.49-.396c.318-.242.553-.646 1.022-1.453c.47-.807.704-1.21.757-1.605a2 2 0 0 0-.4-1.479c-.148-.192-.357-.353-.68-.555c-.477-.297-.783-.803-.783-1.361s.306-1.064.782-1.36c.324-.203.533-.364.682-.556a2 2 0 0 0 .399-1.479c-.053-.394-.287-.798-.757-1.605s-.704-1.21-1.022-1.453a2.03 2.03 0 0 0-1.49-.396c-.242.032-.487.13-.825.308a1.64 1.64 0 0 1-1.58-.008a1.62 1.62 0 0 1-.795-1.353c-.015-.38-.051-.64-.145-.863a2 2 0 0 0-1.09-1.083M12.5 15c1.67 0 3.023-1.343 3.023-3S14.169 9 12.5 9s-3.023 1.343-3.023 3s1.354 3 3.023 3" clip-rule="evenodd"/></svg>{func.get_translate("Settings")}</a>
        </li>
    </ul>

</section>

<style>
    .section-side_foot {
        position: fixed;
        z-index: 0;
        width: 220px;
        max-height: 90px;
        min-height: 40px;
        bottom: 0;
        left: 0;
    }

    .side_foot-ul{
        position: absolute;
        bottom: 0;
        left: 0;
        padding: 0 2px;
        width: 100%;
    }
    .side_foot-menu-li{
        max-height: calc(72px + 10px);
        overflow: hidden;
        clear: both;
    }
    .side_foot-menu-a{
        line-height: 24px;
        padding: 8px 8px;
        width: 100%;
        display: block;
        clear: both;
    }
    .side_foot-menu-a-active{
        background: rgba(200, 200, 200, 0.2);
        color: var(--color-blue-400);
    }

</style>