import {browser} from "$app/environment";
import func from "$lib/common/func.svelte.js";

export const watch_theme_model_data = $state({
    theme_model: "", // dark light
});

// 检测主题变化
if (browser){
    //
    watch_theme_model_data.theme_model = func.get_theme_model();
    //
    let theme_event = window.matchMedia('(prefers-color-scheme: dark)');
    theme_event.addEventListener('change', function (event){
        watch_theme_model_data.theme_model = func.get_theme_model();
    });
}else{
    //
}