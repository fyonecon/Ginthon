<script lang="ts">
    import { resolve } from '$app/paths';
    import { page } from '$app/state';
    import func from "../common/func.svelte.js";
    import { afterNavigate, beforeNavigate } from "$app/navigation";
    import config from "../config";


    // 页面数据
    let route = $state(func.get_route());
    let user_nickname = $state("...");


    // 本页面函数：Svelte的HTML组件onXXX=中正确调用：={()=>def.xxx()}
    const def = {
        //
    };


    // 刷新页面数据
    afterNavigate(() => {
        route = func.get_route();
        user_nickname = func.get_local_data(config.app.app_class + "user_nickname");
        if (!user_nickname) {
            user_nickname = "("+func.get_translate("user_need_login")+")";
        }
    });


</script>

<section class="section-side_setting select-none bg-neutral-200 dark:bg-neutral-800">
    <!--   -->
    <ul class="side_setting-ul select-none font-text">
        <li class="li-group-user select-none click">
            <a class="side_setting-menu-a border-radius break {(route==='/settings' || route.indexOf('/settings/') === 0)?' side_setting-menu-a-active ':' '} click" href={resolve(func.url_path('/settings'))} >
                <svg class="li-group-user-avatar font-text" xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 16 16"><path fill="#2A7DFF" d="M11 7c0 1.66-1.34 3-3 3S5 8.66 5 7s1.34-3 3-3s3 1.34 3 3"/><path fill="#2A7DFF" fill-rule="evenodd" d="M16 8c0 4.42-3.58 8-8 8s-8-3.58-8-8s3.58-8 8-8s8 3.58 8 8M4 13.75C4.16 13.484 5.71 11 7.99 11c2.27 0 3.83 2.49 3.99 2.75A6.98 6.98 0 0 0 14.99 8c0-3.87-3.13-7-7-7s-7 3.13-7 7c0 2.38 1.19 4.49 3.01 5.75" clip-rule="evenodd"/></svg>
                <div class="li-group-user-info">
                    <div class="li-group-user-info-item li-group-user-nickname font-text break-ellipsis">
                        {user_nickname}
                    </div>
                    <div class="li-group-user-info-item li-group-user-tips font-mini break-ellipsis">
                        {func.get_translate("user_tips")}
                    </div>
                </div>
            </a>
        </li>
    </ul>

</section>

<style>
    .section-side_setting {
        position: fixed;
        z-index: 0;
        width: 220px;
        height: 70px;
        bottom: 0;
        left: 0;
        border-bottom-right-radius: 10px;
        border-bottom-left-radius: 10px;
    }

    .side_setting-ul{
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
    }

    .li-group-user{
        clear: both;
        padding: 10px 10px;
        overflow: hidden;
    }
    .li-group-user-avatar{
        float: left;
        height: 40px;
        line-height: 40px;
        width: 40px;
        overflow: hidden;
        background-size: cover;
        background-position: center;
        border-radius: 50%;
    }
    .li-group-user-info{
        float: left;
        height: 40px;
        width: 140px;
        overflow: hidden;
        padding-left: 5px;
    }
    .li-group-user-info-item{
        overflow: hidden;
    }
    .li-group-user-nickname{
        height: 26px;
        line-height: 26px;
    }
    .li-group-user-tips{
        height: 14px;
        line-height: 14px;
    }
    .li-group-user-tips{
        opacity: 0.5;
    }

    .side_setting-menu-a{
        display: block;
        clear: both;
        height: 50px;
        padding: 5px 5px;
    }
    .side_setting-menu-a-active{
        background: rgba(160,160,160, 0.3) !important;
        /*color: var(--color-blue-400);*/
    }
    .side_setting-menu-a:hover{
        background: rgba(160,160,160, 0.2);
    }

</style>