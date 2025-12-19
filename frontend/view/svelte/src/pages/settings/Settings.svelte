<script lang="ts">
    import { resolve } from '$app/paths';
    import { page } from '$app/state';
    import func from "../../common/func.svelte.js";
    import config from "../../config.js";
    import { afterNavigate, beforeNavigate } from "$app/navigation";
    import { Dialog, Portal } from '@skeletonlabs/skeleton-svelte';
    import {onMount} from "svelte";


    // 本页面数据
    const animation = 'transition transition-discrete opacity-0 translate-y-[100px] starting:data-[state=open]:opacity-0 starting:data-[state=open]:translate-y-[100px] data-[state=open]:opacity-100 data-[state=open]:translate-y-0';
    let route = $state(func.get_route());
    let language_index = $state(""); // 语言选中
    const key_theme_model = config.app.app_class+"theme_model";
    let mode = func.get_local_data(key_theme_model);
    let theme_model = $state(mode?mode:""); // 主题选中
    let app_version = $state(config.app.app_version);


    // 本页面函数
    const def = {
        choose_language: function (lang=""){  // 显示和设置语言
            let that = this;
            //
            if (lang.length >= 2) {
                func.set_local_data(config.app.app_class + "language_index", lang);
            }
            language_index = that.now_language(); // 更新选中
            func.open_url_no_cache();
            return func.get_local_data(config.app.app_class + "language_index");
        },
        now_language: function () { // 已选的语言
            let that = this;
            //
            let the_language_index = func.get_local_data(config.app.app_class + "language_index");
            return the_language_index?the_language_index:func.get_lang_index("");
        },
        choose_theme_model: function (mode){ // 选择主题
            let that = this;
            //
            theme_model = mode;
            if (!mode){ // 系统默认
                func.set_local_data(key_theme_model, "");
                document.documentElement.setAttribute('data-mode', func.get_theme_model());
            }else{ // 手动设置
                func.set_local_data(key_theme_model, mode);
                document.documentElement.setAttribute('data-mode', mode);
            }
        },
    };


    // 刷新页面数据
    afterNavigate(() => {
        language_index = def.now_language(); // 更新选中
        mode = func.get_local_data(key_theme_model);
        theme_model = mode?mode:"";
    });


    // 页面装载完成后，只运行一次
    onMount(() => {
        //
    });


</script>

<div>
    <ul class="ul-group font-text">
        <li class="li-group select-none">
            <div class="li-group-title break">
                <svg class="svg-icon" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><g fill="none" fill-rule="evenodd"><path d="m12.594 23.258l-.012.002l-.071.035l-.02.004l-.014-.004l-.071-.036q-.016-.004-.024.006l-.004.01l-.017.428l.005.02l.01.013l.104.074l.015.004l.012-.004l.104-.074l.012-.016l.004-.017l-.017-.427q-.004-.016-.016-.018m.264-.113l-.014.002l-.184.093l-.01.01l-.003.011l.018.43l.005.012l.008.008l.201.092q.019.005.029-.008l.004-.014l-.034-.614q-.005-.019-.02-.022m-.715.002a.02.02 0 0 0-.027.006l-.006.014l-.034.614q.001.018.017.024l.015-.002l.201-.093l.01-.008l.003-.011l.018-.43l-.003-.012l-.01-.01z"/><path fill="currentColor" d="M12 2c5.523 0 10 4.477 10 10a9.96 9.96 0 0 1-2.258 6.33l.02.022l-.132.112A9.98 9.98 0 0 1 12 22c-2.95 0-5.6-1.277-7.43-3.307l-.2-.23l-.132-.11l.02-.024A9.96 9.96 0 0 1 2 12C2 6.477 6.477 2 12 2m0 15c-1.86 0-3.541.592-4.793 1.406A7.97 7.97 0 0 0 12 20a7.97 7.97 0 0 0 4.793-1.594A8.9 8.9 0 0 0 12 17m0-13a8 8 0 0 0-6.258 12.984C7.363 15.821 9.575 15 12 15s4.637.821 6.258 1.984A8 8 0 0 0 12 4m0 2a4 4 0 1 1 0 8a4 4 0 0 1 0-8m0 2a2 2 0 1 0 0 4a2 2 0 0 0 0-4"/></g></svg>
                {func.get_translate("User")}
            </div>
            <div class="li-group-content">
                <div style="height: 60px;opacity: 0.5;">
                    （User）
                </div>
            </div>
        </li>
        <li class="li-group select-none">
            <div class="li-group-title break">
                <svg class="svg-icon" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="currentColor" d="M13 9h-2V7h2m0 10h-2v-6h2m-1-9A10 10 0 0 0 2 12a10 10 0 0 0 10 10a10 10 0 0 0 10-10A10 10 0 0 0 12 2"/></svg>
                {func.get_translate("app_info")}
            </div>
            <div class="li-group-content">
                <div style="margin-bottom: 5px;">
                    <img src="./launcher.png" style="height: 50px;" alt="Logo">
                </div>
                <div>
                    <a title="See Detail" class="font-blue click" href={resolve(func.url_path('/settings/about'))} >
                        {func.get_translate("a_click_tip_see_detail")} - v{app_version}
                    </a>
                </div>
            </div>
        </li>
        <li class="li-group">
            <div class="li-group-title break">
                <svg class="svg-icon" xmlns="http://www.w3.org/2000/svg" width="20" height="25" viewBox="0 0 640 512"><path fill="currentColor" d="M0 128c0-35.3 28.7-64 64-64h512c35.3 0 64 28.7 64 64v256c0 35.3-28.7 64-64 64H64c-35.3 0-64-28.7-64-64zm320 0v256h256V128zm-141.7 47.9c-3.2-7.2-10.4-11.9-18.3-11.9s-15.1 4.7-18.3 11.9l-64 144c-4.5 10.1.1 21.9 10.2 26.4s21.9-.1 26.4-10.2l8.9-20.1h73.6l8.9 20.1c4.5 10.1 16.3 14.6 26.4 10.2s14.6-16.3 10.2-26.4zM160 233.2l19 42.8h-38zM448 164c11 0 20 9 20 20v4h60c11 0 20 9 20 20s-9 20-20 20h-2l-1.6 4.5c-8.9 24.4-22.4 46.6-39.6 65.4c.9.6 1.8 1.1 2.7 1.6l18.9 11.3c9.5 5.7 12.5 18 6.9 27.4s-18 12.5-27.4 6.9L467 333.8c-4.5-2.7-8.8-5.5-13.1-8.5c-10.6 7.5-21.9 14-34 19.4l-3.6 1.6c-10.1 4.5-21.9-.1-26.4-10.2s.1-21.9 10.2-26.4l3.6-1.6c6.4-2.9 12.6-6.1 18.5-9.8L410 286.1c-7.8-7.8-7.8-20.5 0-28.3s20.5-7.8 28.3 0l14.6 14.6l.5.5c12.4-13.1 22.5-28.3 29.8-45l-35.2.1h-72c-11 0-20-9-20-20s9-20 20-20h52v-4c0-11 9-20 20-20"/></svg>
                语言/Languages
            </div>
            <div class="li-group-content break">
                <!--         en       -->
                <Dialog>
                    <Dialog.Trigger class="btn btn-sm select-none preset-outlined-surface-500 font-text float-left mr-[10px] mb-[10px]">
                        <svg class="{(language_index==='en')?'':'hide'} font-green" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 48 48"><path fill="currentColor" fill-rule="evenodd" d="M24 44c11.046 0 20-8.954 20-20S35.046 4 24 4S4 12.954 4 24s8.954 20 20 20m10.742-26.33a1 1 0 1 0-1.483-1.34L21.28 29.567l-6.59-6.291a1 1 0 0 0-1.382 1.446l7.334 7l.743.71l.689-.762z" clip-rule="evenodd"/></svg>
                        English
                    </Dialog.Trigger>
                    <Portal>
                        <Dialog.Backdrop class="fixed inset-0 z-50 bg-surface-50-950/80" />
                        <Dialog.Positioner class="fixed inset-0 z-50 flex justify-center items-center font-text">
                            <Dialog.Content class="card w-full max-w-xs p-4 space-y-4 shadow-xl {animation} px-[10px] py-[10px] border-radius bg-neutral-100 dark:bg-neutral-800">
                                <header class="flex justify-between items-center">
                                    <Dialog.Title class="font-title font-bold">⚠️</Dialog.Title>
                                </header>
                                <Dialog.Description class="font-text" >
                                    {func.get_translate("confirm_change_language_tip", "en")}
                                </Dialog.Description>
                                <footer class="flex justify-center gap-10 select-none  px-[10px] py-[10px]">
                                    <Dialog.CloseTrigger class="btn btn-base preset-tonal font-title">{func.get_translate("btn_cancel")}</Dialog.CloseTrigger>
                                    <button title="Save" type="button" class="btn btn-base preset-filled-primary-500 font-title" onclick={()=>def.choose_language("en")}>{func.get_translate("btn_save")}</button>
                                </footer>
                            </Dialog.Content>
                        </Dialog.Positioner>
                    </Portal>
                </Dialog>
                <!--         zh       -->
                <Dialog>
                    <Dialog.Trigger class="btn btn-sm select-none preset-outlined-surface-500 font-text float-left mr-[10px] mb-[10px]">
                        <svg class="{(language_index==='zh')?'':'hide'} font-green" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 48 48"><path fill="currentColor" fill-rule="evenodd" d="M24 44c11.046 0 20-8.954 20-20S35.046 4 24 4S4 12.954 4 24s8.954 20 20 20m10.742-26.33a1 1 0 1 0-1.483-1.34L21.28 29.567l-6.59-6.291a1 1 0 0 0-1.382 1.446l7.334 7l.743.71l.689-.762z" clip-rule="evenodd"/></svg>
                        中文
                    </Dialog.Trigger>
                    <Portal>
                        <Dialog.Backdrop class="fixed inset-0 z-50 bg-surface-50-950/80" />
                        <Dialog.Positioner class="fixed inset-0 z-50 flex justify-center items-center font-text">
                            <Dialog.Content class="card bg-neutral-100 dark:bg-neutral-800 w-full max-w-xs p-4 space-y-4 shadow-xl {animation}  px-[10px] py-[10px] border-radius">
                                <header class="flex justify-between items-center">
                                    <Dialog.Title class="font-title font-bold">⚠️</Dialog.Title>
                                </header>
                                <Dialog.Description class="font-text" >
                                    {func.get_translate("confirm_change_language_tip", "zh")}
                                </Dialog.Description>
                                <footer class="flex justify-center gap-10 select-none  px-[10px] py-[10px]">
                                    <Dialog.CloseTrigger class="btn btn-base preset-tonal font-title">{func.get_translate("btn_cancel")}</Dialog.CloseTrigger>
                                    <button title="Save" type="button" class="btn btn-base preset-filled-primary-500 font-title" onclick={()=>def.choose_language("zh")}>{func.get_translate("btn_save")}</button>
                                </footer>
                            </Dialog.Content>
                        </Dialog.Positioner>
                    </Portal>
                </Dialog>
                <!--        jp        -->
                <Dialog>
                    <Dialog.Trigger class="btn btn-sm select-none preset-outlined-surface-500 font-text float-left mr-[10px] mb-[10px] hide">
                        <svg class="{(language_index==='jp')?'':'hide'} font-green" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 48 48"><path fill="currentColor" fill-rule="evenodd" d="M24 44c11.046 0 20-8.954 20-20S35.046 4 24 4S4 12.954 4 24s8.954 20 20 20m10.742-26.33a1 1 0 1 0-1.483-1.34L21.28 29.567l-6.59-6.291a1 1 0 0 0-1.382 1.446l7.334 7l.743.71l.689-.762z" clip-rule="evenodd"/></svg>
                        日本語
                    </Dialog.Trigger>
                    <Portal>
                        <Dialog.Backdrop class="fixed inset-0 z-50 bg-surface-50-950/80" />
                        <Dialog.Positioner class="fixed inset-0 z-50 flex justify-center items-center font-text">
                            <Dialog.Content class="card bg-neutral-100 dark:bg-neutral-800 w-full max-w-xs p-4 space-y-4 shadow-xl {animation}  px-[10px] py-[10px] border-radius">
                                <header class="flex justify-between items-center">
                                    <Dialog.Title class="font-title font-bold">⚠️</Dialog.Title>
                                </header>
                                <Dialog.Description class="font-text" >
                                    {func.get_translate("confirm_change_language_tip", "jp")}
                                </Dialog.Description>
                                <footer class="flex justify-center gap-10 select-none  px-[10px] py-[10px]">
                                    <Dialog.CloseTrigger class="btn btn-base preset-tonal font-title">{func.get_translate("btn_cancel")}</Dialog.CloseTrigger>
                                    <button title="Save" type="button" class="btn btn-base preset-filled-primary-500 font-title" onclick={()=>def.choose_language("jp")}>{func.get_translate("btn_save")}</button>
                                </footer>
                            </Dialog.Content>
                        </Dialog.Positioner>
                    </Portal>
                </Dialog>
                <!--         fr       -->
                <Dialog>
                    <Dialog.Trigger class="btn btn-sm select-none preset-outlined-surface-500 font-text float-left mr-[10px] mb-[10px] hide">
                        <svg class="{(language_index==='fr')?'':'hide'} font-green" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 48 48"><path fill="currentColor" fill-rule="evenodd" d="M24 44c11.046 0 20-8.954 20-20S35.046 4 24 4S4 12.954 4 24s8.954 20 20 20m10.742-26.33a1 1 0 1 0-1.483-1.34L21.28 29.567l-6.59-6.291a1 1 0 0 0-1.382 1.446l7.334 7l.743.71l.689-.762z" clip-rule="evenodd"/></svg>
                        Français
                    </Dialog.Trigger>
                    <Portal>
                        <Dialog.Backdrop class="fixed inset-0 z-50 bg-surface-50-950/80" />
                        <Dialog.Positioner class="fixed inset-0 z-50 flex justify-center items-center font-text">
                            <Dialog.Content class="card bg-neutral-100 dark:bg-neutral-800 w-full max-w-xs p-4 space-y-4 shadow-xl {animation}  px-[10px] py-[10px] border-radius">
                                <header class="flex justify-between items-center">
                                    <Dialog.Title class="font-title font-bold">⚠️</Dialog.Title>
                                </header>
                                <Dialog.Description class="font-text" >
                                    {func.get_translate("confirm_change_language_tip", "fr")}
                                </Dialog.Description>
                                <footer class="flex justify-center gap-10 select-none  px-[10px] py-[10px]">
                                    <Dialog.CloseTrigger class="btn btn-base preset-tonal font-title">{func.get_translate("btn_cancel")}</Dialog.CloseTrigger>
                                    <button title="Save" type="button" class="btn btn-base preset-filled-primary-500 font-title" onclick={()=>def.choose_language("fr")}>{func.get_translate("btn_save")}</button>
                                </footer>
                            </Dialog.Content>
                        </Dialog.Positioner>
                    </Portal>
                </Dialog>
                <!--        de        -->
                <Dialog>
                    <Dialog.Trigger class="btn btn-sm select-none preset-outlined-surface-500 font-text float-left mr-[10px] mb-[10px] hide">
                        <svg class="{(language_index==='de')?'':'hide'} font-green" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 48 48"><path fill="currentColor" fill-rule="evenodd" d="M24 44c11.046 0 20-8.954 20-20S35.046 4 24 4S4 12.954 4 24s8.954 20 20 20m10.742-26.33a1 1 0 1 0-1.483-1.34L21.28 29.567l-6.59-6.291a1 1 0 0 0-1.382 1.446l7.334 7l.743.71l.689-.762z" clip-rule="evenodd"/></svg>
                        Deutsch
                    </Dialog.Trigger>
                    <Portal>
                        <Dialog.Backdrop class="fixed inset-0 z-50 bg-surface-50-950/80" />
                        <Dialog.Positioner class="fixed inset-0 z-50 flex justify-center items-center font-text">
                            <Dialog.Content class="card bg-neutral-100 dark:bg-neutral-800 w-full max-w-xs p-4 space-y-4 shadow-xl {animation}  px-[10px] py-[10px] border-radius">
                                <header class="flex justify-between items-center">
                                    <Dialog.Title class="font-title font-bold">⚠️</Dialog.Title>
                                </header>
                                <Dialog.Description class="font-text" >
                                    {func.get_translate("confirm_change_language_tip", "de")}
                                </Dialog.Description>
                                <footer class="flex justify-center gap-10 select-none  px-[10px] py-[10px]">
                                    <Dialog.CloseTrigger class="btn btn-base preset-tonal font-title">{func.get_translate("btn_cancel")}</Dialog.CloseTrigger>
                                    <button title="Save" type="button" class="btn btn-base preset-filled-primary-500 font-title" onclick={()=>def.choose_language("de")}>{func.get_translate("btn_save")}</button>
                                </footer>
                            </Dialog.Content>
                        </Dialog.Positioner>
                    </Portal>
                </Dialog>
                <!--        ru        -->
                <Dialog>
                    <Dialog.Trigger class="btn btn-sm select-none preset-outlined-surface-500 font-text float-left mr-[10px] mb-[10px] hide">
                        <svg class="{(language_index==='ru')?'':'hide'} font-green" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 48 48"><path fill="currentColor" fill-rule="evenodd" d="M24 44c11.046 0 20-8.954 20-20S35.046 4 24 4S4 12.954 4 24s8.954 20 20 20m10.742-26.33a1 1 0 1 0-1.483-1.34L21.28 29.567l-6.59-6.291a1 1 0 0 0-1.382 1.446l7.334 7l.743.71l.689-.762z" clip-rule="evenodd"/></svg>
                        Русский язык
                    </Dialog.Trigger>
                    <Portal>
                        <Dialog.Backdrop class="fixed inset-0 z-50 bg-surface-50-950/80" />
                        <Dialog.Positioner class="fixed inset-0 z-50 flex justify-center items-center font-text">
                            <Dialog.Content class="card bg-neutral-100 dark:bg-neutral-800 w-full max-w-xs p-4 space-y-4 shadow-xl {animation}  px-[10px] py-[10px] border-radius">
                                <header class="flex justify-between items-center">
                                    <Dialog.Title class="font-title font-bold">⚠️</Dialog.Title>
                                </header>
                                <Dialog.Description class="font-text" >
                                    {func.get_translate("confirm_change_language_tip", "ru")}
                                </Dialog.Description>
                                <footer class="flex justify-center gap-10 select-none  px-[10px] py-[10px]">
                                    <Dialog.CloseTrigger class="btn btn-base preset-tonal font-title">{func.get_translate("btn_cancel")}</Dialog.CloseTrigger>
                                    <button title="Save" type="button" class="btn btn-base preset-filled-primary-500 font-title" onclick={()=>def.choose_language("ru")}>{func.get_translate("btn_save")}</button>
                                </footer>
                            </Dialog.Content>
                        </Dialog.Positioner>
                    </Portal>
                </Dialog>
                <!--         es       -->
                <Dialog>
                    <Dialog.Trigger class="btn btn-sm select-none preset-outlined-surface-500 font-text float-left mr-[10px] mb-[10px] hide">
                        <svg class="{(language_index==='es')?'':'hide'} font-green" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 48 48"><path fill="currentColor" fill-rule="evenodd" d="M24 44c11.046 0 20-8.954 20-20S35.046 4 24 4S4 12.954 4 24s8.954 20 20 20m10.742-26.33a1 1 0 1 0-1.483-1.34L21.28 29.567l-6.59-6.291a1 1 0 0 0-1.382 1.446l7.334 7l.743.71l.689-.762z" clip-rule="evenodd"/></svg>
                        Español
                    </Dialog.Trigger>
                    <Portal>
                        <Dialog.Backdrop class="fixed inset-0 z-50 bg-surface-50-950/80" />
                        <Dialog.Positioner class="fixed inset-0 z-50 flex justify-center items-center font-text">
                            <Dialog.Content class="card bg-neutral-100 dark:bg-neutral-800 w-full max-w-xs p-4 space-y-4 shadow-xl {animation}  px-[10px] py-[10px] border-radius">
                                <header class="flex justify-between items-center">
                                    <Dialog.Title class="font-title font-bold">⚠️</Dialog.Title>
                                </header>
                                <Dialog.Description class="font-text" >
                                    {func.get_translate("confirm_change_language_tip", "es")}
                                </Dialog.Description>
                                <footer class="flex justify-center gap-10 select-none  px-[10px] py-[10px]">
                                    <Dialog.CloseTrigger class="btn btn-base preset-tonal font-title">{func.get_translate("btn_cancel")}</Dialog.CloseTrigger>
                                    <button title="Save" type="button" class="btn btn-base preset-filled-primary-500 font-title" onclick={()=>def.choose_language("es")}>{func.get_translate("btn_save")}</button>
                                </footer>
                            </Dialog.Content>
                        </Dialog.Positioner>
                    </Portal>
                </Dialog>
                <!--        vi        -->
                <Dialog>
                    <Dialog.Trigger class="btn btn-sm select-none preset-outlined-surface-500 font-text float-left mr-[10px] mb-[10px] hide">
                        <svg class="{(language_index==='vi')?'':'hide'} font-green" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 48 48"><path fill="currentColor" fill-rule="evenodd" d="M24 44c11.046 0 20-8.954 20-20S35.046 4 24 4S4 12.954 4 24s8.954 20 20 20m10.742-26.33a1 1 0 1 0-1.483-1.34L21.28 29.567l-6.59-6.291a1 1 0 0 0-1.382 1.446l7.334 7l.743.71l.689-.762z" clip-rule="evenodd"/></svg>
                        Tiếng Việt
                    </Dialog.Trigger>
                    <Portal>
                        <Dialog.Backdrop class="fixed inset-0 z-50 bg-surface-50-950/80" />
                        <Dialog.Positioner class="fixed inset-0 z-50 flex justify-center items-center font-text">
                            <Dialog.Content class="card bg-neutral-100 dark:bg-neutral-800 w-full max-w-xs p-4 space-y-4 shadow-xl {animation}  px-[10px] py-[10px] border-radius">
                                <header class="flex justify-between items-center">
                                    <Dialog.Title class="font-title font-bold">⚠️</Dialog.Title>
                                </header>
                                <Dialog.Description class="font-text" >
                                    {func.get_translate("confirm_change_language_tip", "vi")}
                                </Dialog.Description>
                                <footer class="flex justify-center gap-10 select-none  px-[10px] py-[10px]">
                                    <Dialog.CloseTrigger class="btn btn-base preset-tonal font-title">{func.get_translate("btn_cancel")}</Dialog.CloseTrigger>
                                    <button title="Save" type="button" class="btn btn-base preset-filled-primary-500 font-title" onclick={()=>def.choose_language("vi")}>{func.get_translate("btn_save")}</button>
                                </footer>
                            </Dialog.Content>
                        </Dialog.Positioner>
                    </Portal>
                </Dialog>

            </div>
        </li>

        <li class="li-group">
            <div class="li-group-title break">
                <svg class="svg-icon" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><g fill="none"><path fill="currentColor" d="M2.75 12A9.25 9.25 0 0 0 12 21.25V2.75A9.25 9.25 0 0 0 2.75 12"/><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 21.25a9.25 9.25 0 0 0 0-18.5m0 18.5a9.25 9.25 0 0 1 0-18.5m0 18.5V2.75"/></g></svg>
                {func.get_translate("ThemeModel")}
            </div>
            <div class="li-group-content">
                <button class="btn btn-sm select-none preset-outlined-surface-500 font-text float-left mr-[10px] mb-[10px]" onclick={()=>def.choose_theme_model('')}>
                    <svg class="{(theme_model==='')?'':'hide'} font-green" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 48 48"><path fill="currentColor" fill-rule="evenodd" d="M24 44c11.046 0 20-8.954 20-20S35.046 4 24 4S4 12.954 4 24s8.954 20 20 20m10.742-26.33a1 1 0 1 0-1.483-1.34L21.28 29.567l-6.59-6.291a1 1 0 0 0-1.382 1.446l7.334 7l.743.71l.689-.762z" clip-rule="evenodd"/></svg>
                    {func.get_translate("sys_default")}
                </button>
                <button class="btn btn-sm select-none preset-outlined-surface-500 font-text float-left mr-[10px] mb-[10px]" onclick={()=>def.choose_theme_model('light')}>
                    <svg class="{(theme_model==='light')?'':'hide'} font-green" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 48 48"><path fill="currentColor" fill-rule="evenodd" d="M24 44c11.046 0 20-8.954 20-20S35.046 4 24 4S4 12.954 4 24s8.954 20 20 20m10.742-26.33a1 1 0 1 0-1.483-1.34L21.28 29.567l-6.59-6.291a1 1 0 0 0-1.382 1.446l7.334 7l.743.71l.689-.762z" clip-rule="evenodd"/></svg>
                    {func.get_translate("theme_model_light")}
                </button>
                <button class="btn btn-sm select-none preset-outlined-surface-500 font-text float-left mr-[10px] mb-[10px]" onclick={()=>def.choose_theme_model('dark')}>
                    <svg class="{(theme_model==='dark')?'':'hide'} font-green" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 48 48"><path fill="currentColor" fill-rule="evenodd" d="M24 44c11.046 0 20-8.954 20-20S35.046 4 24 4S4 12.954 4 24s8.954 20 20 20m10.742-26.33a1 1 0 1 0-1.483-1.34L21.28 29.567l-6.59-6.291a1 1 0 0 0-1.382 1.446l7.334 7l.743.71l.689-.762z" clip-rule="evenodd"/></svg>
                    {func.get_translate("theme_model_dark")}
                </button>
            </div>
        </li>

    </ul>
</div>