import {browser} from "$app/environment";
import func from "$lib/common/func.svelte.js";
import config from "../../config.js";

export const watch_theme_model_data = $state({
    theme_model: "", // dark light
});

function auto_set_heme_model() { // 自动切换主题
    const key_theme_model = config.app.app_class+"theme_model";
    let mode = func.get_local_data(key_theme_model);
    if (!mode) {
        let light = window.matchMedia('(prefers-color-scheme: light)').matches;
        if (light) {
            mode = 'light';
        }else {
            mode = 'dark';
        }
    }
    document.documentElement.setAttribute('data-mode', mode);
}

// 检测主题变化
if (browser){
    // 初始化
    watch_theme_model_data.theme_model = func.get_theme_model();
    auto_set_heme_model();
    // 检测
    let theme_event = window.matchMedia('(prefers-color-scheme: dark)');
    theme_event.addEventListener('change', function (event){
        watch_theme_model_data.theme_model = func.get_theme_model();
        auto_set_heme_model();
    });
}else{
    //
}