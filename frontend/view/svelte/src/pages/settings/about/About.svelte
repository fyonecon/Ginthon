<script lang="ts">
    import { resolve } from '$app/paths';
    import { page } from '$app/state';
    import func from "../../../common/func.svelte.js";
    import config from "../../../config.js";
    import { afterNavigate, beforeNavigate } from "$app/navigation";
    import {browser} from "$app/environment";
    import {watch_theme_model_data} from "../../../stores/watch_theme_model.store.svelte.js";


    // 页面数据
    let route = $state(func.get_route());
    let app_uid = $state(func.get_app_uid());
    let user_agent = $state(func.get_agent());
    let href = $state(func.get_href());
    let params = $state(func.get_params());
    let languages = $state(navigator.languages);
    let theme_model = $state(watch_theme_model_data.theme_model);
    let language_index = $state(func.get_local_data(config.app.app_class + "language_index"));

    // 打开默认浏览器
    function open_url_with_default_browser(url="", target="_self") {
        func.js_call_py_or_go("open_url_with_default_browser", {
            url: url,
            target: target,
        }).then(result => {});
    }

    // 路由变化之后
    afterNavigate(() => {
        const key_theme_model = config.app.app_class + "theme_model";
        let mode = func.get_local_data(key_theme_model);
        theme_model = mode?mode:watch_theme_model_data.theme_model;
    });

</script>

<div>
    <ul class="ul-group font-text select-text">
        <li class="li-group">
            <div class="li-group-title break">
                {func.get_translate("About")}
            </div>
            <div class="li-group-content">
                {config.app.app_name} UI v{config.app.app_version}
            </div>
        </li>
        <li class="li-group select-none">
            <div class="li-group-title break">
                App UID
            </div>
            <div class="li-group-content break">
                {app_uid?app_uid:"-"}
            </div>
        </li>
        <li class="li-group select-text">
            <div class="li-group-title break">
                User Agent
            </div>
            <div class="li-group-content break">
                {user_agent}
            </div>
        </li>
        <li class="li-group select-none">
            <div class="li-group-title break">
                Href
            </div>
            <div class="li-group-content break">
                <span class="font-orange">Only Local: </span> {href}
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
        <li class="li-group select-none">
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
            <div class="li-group-content break">
                {languages}
            </div>
        </li>
        <li class="li-group">
            <div class="li-group-title break">
                Showing Language
            </div>
            <div class="li-group-content break">
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
        <li class="li-group select-text">
            <div class="li-group-title break">
                Framework
            </div>
            <div class="li-group-content break">
                <button type="button" class="a-btn font-blue click" onclick={()=>open_url_with_default_browser("https://github.com/fyonecon/Ginthon?ap=app", "_blank")}>Ginthon(Python)</button>
                <button type="button" class="a-btn font-blue click" onclick={()=>open_url_with_default_browser("https://github.com/fyonecon/Waigo?ap=app", "_blank")}>Waigo(Golang)</button>
            </div>
        </li>
        <li class="li-group">
            <div class="li-group-title break">
                UI
            </div>
            <div class="li-group-content break">
                <button title="Open" type="button" class="a-btn font-blue click" onclick={()=>open_url_with_default_browser("https://svelte.js.cn/docs/svelte/overview", "_blank")}>SvelteKit</button>
                <button title="Open" type="button" class="a-btn font-blue click" onclick={()=>open_url_with_default_browser("https://www.skeleton.dev/docs/svelte/guides/mode", "_blank")}>SkeletonUI</button>
                <button title="Open" type="button" class="a-btn font-blue click" onclick={()=>open_url_with_default_browser("https://www.tailwindcss.cn/docs/installation", "_blank")}>Tailwind CSS</button>
                <button title="Open" type="button" class="a-btn font-blue click" onclick={()=>open_url_with_default_browser("https://icon-sets.iconify.design/solar/", "_blank")}>Iconify SVG</button>
            </div>
        </li>
    </ul>
</div>