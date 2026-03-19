<script lang="ts">
    import { resolve } from '$app/paths';
    import { page } from '$app/state';
    import func from "../common/func.svelte.js";
    import { afterNavigate, beforeNavigate } from "$app/navigation";
    import { side_tab_data } from '../stores/side_tab.store.svelte.js';
    import {browser_ok, runtime_ok} from "../common/middleware.svelte";


    // 本页面参数
    let route = $state(func.get_route());
    let tab_data: any[] = $state([]);
    const tab_data_array: any[] = [
        {
            order: 1, // 排序，数字越小越前面
            icon: '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 20"><path fill="currentColor" fill-rule="evenodd" d="M2.52 7.823C2 8.77 2 9.915 2 12.203v1.522c0 3.9 0 5.851 1.172 7.063S6.229 22 10 22h4c3.771 0 5.657 0 6.828-1.212S22 17.626 22 13.725v-1.521c0-2.289 0-3.433-.52-4.381c-.518-.949-1.467-1.537-3.364-2.715l-2-1.241C14.111 2.622 13.108 2 12 2s-2.11.622-4.116 1.867l-2 1.241C3.987 6.286 3.038 6.874 2.519 7.823m6.927 7.575a.75.75 0 1 0-.894 1.204A5.77 5.77 0 0 0 12 17.75a5.77 5.77 0 0 0 3.447-1.148a.75.75 0 1 0-.894-1.204A4.27 4.27 0 0 1 12 16.25a4.27 4.27 0 0 1-2.553-.852" clip-rule="evenodd"/></svg>', // 图标，20 px
            title: func.get_translate("Home"), // 名字，可视最大8个字母
            route: "/home", // 对应的route名字，"/"，"/purehome"
            href: func.url_path('/home'), // 跳转地址，"./"，"./purehome"
        },
        {
            order: 4, // 排序，数字越小越前面
            icon: '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="24" viewBox="0 0 32 32"><g fill="none"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-miterlimit="10" d="M3 8.02a8.94 8.94 0 0 0 7.47 7l.26.04m18.6-7.04a8.94 8.94 0 0 1-7.47 7l-.26.04m7.73 9.61a8.94 8.94 0 0 0-7.47-7l-.26-.04M3 24.67a8.94 8.94 0 0 1 7.47-7l.26-.04M25.73 3c0 3.39-1.96 6.47-5.04 7.9l-1.76.82M6.6 3c0 3.39 1.96 6.47 5.04 7.9l1.76.82M6.6 29.86c0-3.39 1.96-6.47 5.04-7.9l1.76-.82m12.33 8.72c0-3.39-1.96-6.47-5.04-7.9l-1.76-.82" stroke-width="1"/><path fill="currentColor" d="M16.71 3v2.66h1.37V4.37c0-.75-.61-1.37-1.37-1.37m-1.09 0v2.66h-1.37V4.37c0-.75.61-1.37 1.37-1.37"/><path fill="currentColor" d="M19.31 10.9a3.8 3.8 0 0 0 .68-2.17a3.82 3.82 0 1 0-6.96 2.17a8 8 0 0 0-4.86 7.36c0 4.42 3.58 8 8 8s8-3.58 8-8c0-3.3-2.01-6.13-4.86-7.36"/><path fill="currentColor" d="M26.23 3a.5.5 0 0 0-1 0a8.2 8.2 0 0 1-4.75 7.447l-1.069.497l-.1-.044a3.82 3.82 0 0 0-1.23-5.48V4.37A1.375 1.375 0 0 0 16.709 3v1.948a4 4 0 0 0-1.09.001V3c-.76 0-1.37.62-1.37 1.37v1.057a3.82 3.82 0 0 0-1.22 5.473l-.107.046l-1.072-.5A8.2 8.2 0 0 1 7.1 3a.5.5 0 0 0-1 0a9.2 9.2 0 0 0 5.33 8.353l.398.186a8.04 8.04 0 0 0-2.574 2.698a8.45 8.45 0 0 1-5.765-6.32a.5.5 0 0 0-.978.207a9.45 9.45 0 0 0 6.29 7.018a8 8 0 0 0-.616 2.632a9.45 9.45 0 0 0-5.674 6.792a.5.5 0 0 0 .978.208a8.46 8.46 0 0 1 4.703-5.913a7.96 7.96 0 0 0 1.321 3.84A9.2 9.2 0 0 0 6.1 29.86a.5.5 0 0 0 1 0a8.2 8.2 0 0 1 3.02-6.364a7.98 7.98 0 0 0 6.05 2.764a7.98 7.98 0 0 0 6.046-2.76a8.2 8.2 0 0 1 3.014 6.36a.5.5 0 1 0 1 0c0-2.816-1.28-5.43-3.407-7.154a7.96 7.96 0 0 0 1.325-3.84a8.46 8.46 0 0 1 4.693 5.908a.5.5 0 0 0 .978-.208a9.45 9.45 0 0 0-5.663-6.788a7.9 7.9 0 0 0-.62-2.638a9.45 9.45 0 0 0 6.283-7.016a.5.5 0 1 0-.978-.208a8.45 8.45 0 0 1-5.76 6.32a8.1 8.1 0 0 0-2.578-2.697l.398-.185A9.2 9.2 0 0 0 26.23 3"/></g></svg>', // 图标，20 px
            title: func.get_translate("ITHome"), // 名字，可视最大8个字母
            route: "/it_home", // 对应的route名字，"/"，"/purehome"
            href: func.url_path('/it_home'), // 跳转地址，"./"，"./purehome"
        },
        {
            order: 7, // 排序，数字越小越前面
            icon: '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="24" viewBox="0 0 48 48"><defs><mask id="SVGENzItdvk"><g fill="none" stroke="#fff" stroke-width="4"><path d="M24 44c11.046 0 20-8.954 20-20S35.046 4 24 4S4 12.954 4 24s8.954 20 20 20Z"/><path stroke-linecap="round" stroke-linejoin="round" d="M26 14v14"/><path fill="#555555" stroke-linejoin="round" d="M14 28.666C14 26.64 15.934 25 18.32 25H26v4.334C26 31.36 24.066 33 21.68 33h-3.36C15.934 33 14 31.359 14 29.334z"/><path stroke-linecap="round" stroke-linejoin="round" d="m32 15l-6-1"/></g></mask></defs><path fill="currentColor" d="M0 0h48v48H0z" mask="url(#SVGENzItdvk)"/></svg>', // 图标，20 px
            title: func.get_translate("PlayAudio"), // 名字，可视最大8个字母
            route: "/play_audio", // 对应的route名字，"/"，"/purehome"
            href: func.url_path('/play_audio'), // 跳转地址，"./"，"./purehome"
        },
        {
            order: 3, // 排序，数字越小越前面
            icon: '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20"><path fill="currentColor" d="M13 11h-2v2h2v2h-2v2h2v-2h2v2h2v-2h-2v-2h2v-2h-2v2h-2zM5 5h2v2H5zm0-2a2 2 0 0 0-2 2v2a2 2 0 0 0 2 2h2a2 2 0 0 0 2-2V5a2 2 0 0 0-2-2zm-.75 1.75a.5.5 0 0 1 .5-.5h2.5a.5.5 0 0 1 .5.5v2.5a.5.5 0 0 1-.5.5h-2.5a.5.5 0 0 1-.5-.5zM5 13h2v2H5zm0-2a2 2 0 0 0-2 2v2a2 2 0 0 0 2 2h2a2 2 0 0 0 2-2v-2a2 2 0 0 0-2-2zm-.75 1.75a.5.5 0 0 1 .5-.5h2.5a.5.5 0 0 1 .5.5v2.5a.5.5 0 0 1-.5.5h-2.5a.5.5 0 0 1-.5-.5zM13 5h2v2h-2zm0-2a2 2 0 0 0-2 2v2a2 2 0 0 0 2 2h2a2 2 0 0 0 2-2V5a2 2 0 0 0-2-2zm-.75 1.75a.5.5 0 0 1 .5-.5h2.5a.5.5 0 0 1 .5.5v2.5a.5.5 0 0 1-.5.5h-2.5a.5.5 0 0 1-.5-.5z"/></svg>', // 图标，20 px
            title: func.get_translate("qr"), // 名字，可视最大8个字母
            route: "/qr", // 对应的route名字，"/"，"/purehome"
            href: func.url_path('/qr'), // 跳转地址，"./"，"./purehome"
        },
    ];


    // 本页面函数：Svelte的HTML组件onXXX=中正确调用：={()=>def.xxx()}
    const def = {
        order_tab_data_array: function (tab_data_array: any[]){ // // 根据order大小，从小到大排序，格式 [{order:1}, {order:4}, {order:2}]
            return [...tab_data_array].sort((a, b) => a.order - b.order);
        },
        get_route_info: function(_route="") {  // 将路由转化为翻译的键
            let that = this;
            //
            for (let i=0; i<tab_data.length; i++){
                if (_route === tab_data[i].route){
                    side_tab_data.tab_value = _route;
                    side_tab_data.tab_name = tab_data[i].title;
                    break;
                }
            }
        },
    };


    // 刷新页面数据
    afterNavigate(() => {
        if (!func.support_min_js()){return;}
        if (!runtime_ok() || !browser_ok()){return;} // 系统基础条件检测
        //
        route = func.get_route();
        //
        tab_data = tab_data_array;
        tab_data = def.order_tab_data_array(tab_data);
        def.get_route_info(route);
        //
    });


</script>

<section class="section-side_tab select-none bg-neutral-200 dark:bg-neutral-800">
    <ul class="side_tab-menu-ul scroll-y-style select-none font-text">
        <!---->
        {#each tab_data as item}
            <li class="side_tab-menu-li">
                <a class="side_tab-menu-a border-radius break {(route === item.route)?'side_tab-menu-a-active':''} click" href={resolve(func.url_path(item.href))} >
                    {@html item.icon.replace('<svg ', '<svg class="svg-icon font-blue" ')}
                    {@html item.title}
                </a>
            </li>
        {/each}
    </ul>
</section>

<style>
    .section-side_tab {
        position: fixed;
        z-index: 0;
        width: 220px;
        padding: 0 10px 10px 10px;
        height: calc(100% - 92px - 70px);
        top: 92px;
        left: 0;
    }

    .side_tab-menu-ul{
        width: calc(100% - 8px);
        height: 100%;
        padding-bottom: 90px;
        padding-top: 10px;
        position: absolute;
    }
    .side_tab-menu-li{
        width: 196px;
        max-height: calc(72px + 10px);
        overflow: hidden;
        clear: both;
        margin-bottom: 1px;
    }
    .side_tab-menu-a{
        line-height: 24px;
        padding: 8px 8px;
        width: 100%;
        display: block;
        clear: both;
    }
    .side_tab-menu-a-active{
        background: rgba(160,160,160, 0.3) !important;
        /*color: var(--color-blue-400);*/
    }
    .side_tab-menu-a:hover{
        background: rgba(160,160,160, 0.2);
    }

</style>