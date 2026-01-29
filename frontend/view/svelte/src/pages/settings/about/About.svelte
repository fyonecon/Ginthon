<script lang="ts">
    import { resolve } from '$app/paths';
    import func from "../../../common/func.svelte";
    import config from "../../../config";
    import { afterNavigate} from "$app/navigation";
    import {watch_theme_model_data} from "../../../stores/watch_theme_model.store.svelte";
    import {onMount} from "svelte";
    import {watch_lang_data} from "../../../stores/watch_lang.store.svelte";
    import {browser_ok, runtime_ok} from "../../../common/middleware.svelte";


    // 本页面数据
    let route = $state(func.get_route());
    let app_uid = $state("");
    let user_agent = $state(func.get_agent());
    let href = $state(func.get_href());
    let params = $state(func.get_params());
    let languages = $state(navigator.languages);
    let theme_model = $state("");
    let language_index = $state("");


    // 本页面函数：Svelte的HTML组件onXXX=中正确调用：={()=>def.xxx()}
    const def = {
        //
    };


    // 页面函数执行的入口，实时更新数据
    function page_start(){
        console.log("page_start()=", route);
        // 开始
        func.get_app_uid().then(_app_uid=>{
            app_uid = _app_uid;
        });
        theme_model = watch_theme_model_data.theme_model;
        language_index = watch_lang_data.lang_index;
        //
    }


    // 检测$state()值变化
    $effect(() => {
        //
    });


    // 刷新页面数据
    afterNavigate(() => {
        if (!runtime_ok() || !browser_ok()){return;} // 系统基础条件检测
        //
        page_start();
    });


    // 页面装载完成后，只运行一次
    onMount(() => {
        //
    });


</script>

<div>
    <ul class="ul-group font-text">
        <li class="li-group">
            <div class="li-group-title break">
                {func.get_translate("About")}
            </div>
            <div class="li-group-content select-text">
                {config.app.app_name} UI v{config.app.app_version}
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
            <div class="li-group-content break select-text">
                {user_agent}
            </div>
        </li>
        <li class="li-group">
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
            <div class="li-group-content break select-text">
                {theme_model}
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
    </ul>
</div>