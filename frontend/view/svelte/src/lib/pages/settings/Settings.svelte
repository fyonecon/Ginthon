<script>
    import { resolve } from '$app/paths';
    import { page } from '$app/state';
    import func from "$lib/common/func.svelte.js";
    import config from "$lib/config.js";
    import { afterNavigate, beforeNavigate } from "$app/navigation";
    import { Dialog, Portal } from '@skeletonlabs/skeleton-svelte';


    // 显示和设置语言
    function choose_language(lang=""){
        if (lang.length >= 2) {
            func.set_local_data(config.app.app_class + "language_index", lang);
        }
        language_index = now_language(); // 更新选中
        func.open_url(func.url_path(config.sys.home_route)+"?lang=" + language_index);
        // func.open_url_no_cache(func.url_path(config.sys.home_route)+"?lang=" + language_index);
        return func.get_local_data(config.app.app_class + "language_index");
    }
    //
    function now_language(){
        let the_language_index = func.get_local_data(config.app.app_class + "language_index");
        return the_language_index?the_language_index:func.get_lang_index("");
    }


    // 页面数据
    let route = $state(func.get_route());
    let language_index = $state(now_language()); // 更新选中
    const animation = 'transition transition-discrete opacity-0 translate-y-[100px] starting:data-[state=open]:opacity-0 starting:data-[state=open]:translate-y-[100px] data-[state=open]:opacity-100 data-[state=open]:translate-y-0';



    // 刷新页面数据
    afterNavigate(() => {
        language_index = now_language(); // 更新选中
    });

</script>

<div>
    <ul class="ul-group font-text">
        <li class="li-group">
            <div class="li-group-title break">
                {func.get_translate("About")}
            </div>
            <div class="li-group-content">
                <a title="See Detail" class="font-blue click" href={resolve(func.url_path('/settings/about'))} >{func.get_translate("a_click_tip_see_detail")}</a>
            </div>
        </li>
        <li class="li-group">
            <div class="li-group-title break">
                <svg xmlns="http://www.w3.org/2000/svg" width="22" height="25" viewBox="0 0 640 512"><path fill="currentColor" d="M0 128c0-35.3 28.7-64 64-64h512c35.3 0 64 28.7 64 64v256c0 35.3-28.7 64-64 64H64c-35.3 0-64-28.7-64-64zm320 0v256h256V128zm-141.7 47.9c-3.2-7.2-10.4-11.9-18.3-11.9s-15.1 4.7-18.3 11.9l-64 144c-4.5 10.1.1 21.9 10.2 26.4s21.9-.1 26.4-10.2l8.9-20.1h73.6l8.9 20.1c4.5 10.1 16.3 14.6 26.4 10.2s14.6-16.3 10.2-26.4zM160 233.2l19 42.8h-38zM448 164c11 0 20 9 20 20v4h60c11 0 20 9 20 20s-9 20-20 20h-2l-1.6 4.5c-8.9 24.4-22.4 46.6-39.6 65.4c.9.6 1.8 1.1 2.7 1.6l18.9 11.3c9.5 5.7 12.5 18 6.9 27.4s-18 12.5-27.4 6.9L467 333.8c-4.5-2.7-8.8-5.5-13.1-8.5c-10.6 7.5-21.9 14-34 19.4l-3.6 1.6c-10.1 4.5-21.9-.1-26.4-10.2s.1-21.9 10.2-26.4l3.6-1.6c6.4-2.9 12.6-6.1 18.5-9.8L410 286.1c-7.8-7.8-7.8-20.5 0-28.3s20.5-7.8 28.3 0l14.6 14.6l.5.5c12.4-13.1 22.5-28.3 29.8-45l-35.2.1h-72c-11 0-20-9-20-20s9-20 20-20h52v-4c0-11 9-20 20-20"/></svg>
                语言/Languages
            </div>
            <div class="li-group-content break">
                <!--                -->
                <Dialog>
                    <Dialog.Trigger class="btn btn-sm select-none {(language_index==='en')?'preset-filled-primary-500':'preset-filled'}">English</Dialog.Trigger>
                    <Portal>
                        <Dialog.Backdrop class="fixed inset-0 z-50 bg-surface-50-950/50" />
                        <Dialog.Positioner class="fixed inset-0 z-50 flex justify-center items-center p-4">
                            <Dialog.Content class="card bg-surface-100-900 w-full max-w-xl p-4 space-y-4 shadow-xl {animation}">
                                <header class="flex justify-between items-center">
                                    <Dialog.Title class="text-lg font-bold">⚠️</Dialog.Title>
                                </header>
                                <Dialog.Description>
                                    {func.get_translate("confirm_change_language_tip", "en")}
                                </Dialog.Description>
                                <footer class="flex justify-end gap-2 select-none">
                                    <Dialog.CloseTrigger class="btn preset-tonal">{func.get_translate("btn_cancel")}</Dialog.CloseTrigger>
                                    <button title="Save" type="button" class="btn preset-filled-primary-500" onclick={()=>choose_language("en")}>{func.get_translate("btn_save")}</button>
                                </footer>
                            </Dialog.Content>
                        </Dialog.Positioner>
                    </Portal>
                </Dialog>
                <!--                -->
                <Dialog>
                    <Dialog.Trigger class="btn btn-sm select-none {(language_index==='zh')?'preset-filled-primary-500':'preset-filled'}">中文</Dialog.Trigger>
                    <Portal>
                        <Dialog.Backdrop class="fixed inset-0 z-50 bg-surface-50-950/50" />
                        <Dialog.Positioner class="fixed inset-0 z-50 flex justify-center items-center p-4">
                            <Dialog.Content class="card bg-surface-100-900 w-full max-w-xl p-4 space-y-4 shadow-xl {animation}">
                                <header class="flex justify-between items-center">
                                    <Dialog.Title class="text-lg font-bold">⚠️</Dialog.Title>
                                </header>
                                <Dialog.Description>
                                    {func.get_translate("confirm_change_language_tip", "zh")}
                                </Dialog.Description>
                                <footer class="flex justify-end gap-2 select-none">
                                    <Dialog.CloseTrigger class="btn btn- preset-tonal">{func.get_translate("btn_cancel")}</Dialog.CloseTrigger>
                                    <button title="Save" type="button" class="btn btn- preset-filled-primary-500" onclick={()=>choose_language("zh")}>{func.get_translate("btn_save")}</button>
                                </footer>
                            </Dialog.Content>
                        </Dialog.Positioner>
                    </Portal>
                </Dialog>

            </div>
        </li>
    </ul>
</div>