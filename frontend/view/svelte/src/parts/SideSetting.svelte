<script lang="ts">
    import { resolve } from '$app/paths';
    import { page } from '$app/state';
    import func from "../common/func.svelte.js";
    import { afterNavigate, beforeNavigate } from "$app/navigation";
    import config from "../config";


    // 页面数据
    let route = $state(func.get_route());
    let user_nickname = $state("...");


    // 本页面函数
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
                <div class="li-group-user-avatar font-text" style="background-image: url('../../user.png');" title="Avatar"></div>
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
        background: rgba(180, 180, 180, 0.4);
        /*color: var(--color-blue-400);*/
    }

</style>