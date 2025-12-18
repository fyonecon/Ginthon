<script>
    import func from "$lib/common/func.svelte.js";
    import { page } from '$app/state';
    import { afterNavigate, beforeNavigate } from "$app/navigation";
    import config from "$lib/config.js";
    import { side_tab_data } from '$lib/stores/side_tab.store.svelte.js';

    // 历史记录算法 >>>>>>
    let href = $state(func.get_href());
    let route = $state(func.get_route());
    let params = $state(func.get_params());
    let time = $state(func.get_time_date("YmdHis"));
    // 显示数据
    let before_href = $state('');
    let before_click = $state('hide');
    let next_href = $state('');
    let next_click = $state('hide');
    // 打开链接
    function open_href(href="") {
        if (href.length >= 1){
            func.open_url(href, "_self");
        }else{ // 空
            console.log("空链接");
        }
    }
    // 设置访问历史
    function set_direction_history(now_director_dict) {
        // 回到主页删除历史记录
        if (config.sys.home_route === route){
            func.del_local_data("director_urls");
        }
        // 插入新历史
        let the_direction_urls = func.get_local_data("director_urls");
        let the_direction_urls_array = [];
        if (the_direction_urls) {
            the_direction_urls_array = func.string_to_json(the_direction_urls);
        }
        return new Promise(resolve => {
            if (the_direction_urls_array.length > 0) {
                /*
                * /home - /settings?id=1 - /settings/about - /spider - /settings?id=2
                * 依次添加每个访问href，如果route一样，params不一样，则删除老的route，添加新的route。每次到主路由home就删除历史访问。
                * */
                let now_route = now_director_dict.route;
                let now_params = now_director_dict.params;
                for (let i = 0; i < the_direction_urls_array.length; i++) {
                    let the_route = the_direction_urls_array[i].route;
                    let the_params = the_direction_urls_array[i].params;
                    if (now_route === the_route) { // 已存在路由历史，则删除历史
                        // the_direction_urls_array.splice(i, 1);
                        // console.log("已存在路由=", now_route, i, the_direction_urls_array.length);
                        resolve(the_direction_urls_array);
                        break;
                    }else{
                        if (i === the_direction_urls_array.length - 1) {
                            the_direction_urls_array.push(now_director_dict);
                            func.set_local_data("director_urls", func.json_to_string(the_direction_urls_array));
                            resolve(the_direction_urls_array);
                        }else{
                            //
                        }
                    }
                }
            }else{ // 空记录就新增一个
                func.set_local_data("director_urls", func.json_to_string([now_director_dict]));
                resolve([now_director_dict]);
            }
        });
    }
    // 获取访问历史
    // 在历史记录中找到上一页、下一页
    function get_direction_history(now_director_dict) {
        let the_before_director_dict = {};
        let the_next_director_dict = {};
        //
        let the_direction_urls = func.get_local_data("director_urls");
        let the_direction_urls_array = [];
        if (the_direction_urls) {
            the_direction_urls_array = func.string_to_json(the_direction_urls);
        }
        if (the_direction_urls_array.length > 0){
            let now_route = now_director_dict.route;
            let now_params = now_director_dict.params;
            let len = the_direction_urls_array.length;
            //
            for (let i = 0; i < the_direction_urls_array.length; i++){
                let the_route = the_direction_urls_array[i].route;
                let the_params = the_direction_urls_array[i].params;
                if (now_route === the_route) { // 主路由一样，则删除历史
                    if (len>=2){ // 至少有两个访问记录
                        if (i === 0){ // 第一个 >>>
                            the_before_director_dict = the_direction_urls_array[i];
                            the_next_director_dict = the_direction_urls_array[i+1];
                        }else if (i >= 1 && i < len){
                            the_before_director_dict = the_direction_urls_array[i-1];
                            the_next_director_dict = the_direction_urls_array[i+1];
                        }else{
                            the_before_director_dict = {};
                            the_next_director_dict = {};
                        }
                    }else{ // 为一个的话，则不显示上一页、下一页
                        the_before_director_dict = {};
                        the_next_director_dict = {};
                    }
                    break;
                }
            }
        }else{ // 历史为空
            the_before_director_dict = {};
            the_next_director_dict = {};
        }
        return {
            before_director: the_before_director_dict,
            next_director: the_next_director_dict,
        };
    }
    // 展示页面数据
    function show_direction() {
        //
        href = func.get_href();
        route = func.get_route();
        params = func.get_params();
        time = func.get_time_date("YmdHis");
        //
        let director_dict = { // 当前访问
            href: func.string_to_unicode(href),
            route: route,
            params: func.string_to_unicode(params),
            time: time,
        };
        //
        set_direction_history(director_dict).then(direction_history=>{
            func.console_log("set_direction_history=", direction_history);
            //
            let get_direction = get_direction_history(director_dict);
            //
            try {
                if (get_direction.before_director.route) {
                    let the_before_route = get_direction.before_director.route;
                    let the_before_params = get_direction.before_director.params;
                    before_href = func.url_path(the_before_route+func.unicode_to_string(the_before_params));
                }
            }catch(err){
                before_href = "";
            }
            //
            try {
                if (get_direction.next_director.route) {
                    let the_next_route = get_direction.next_director.route;
                    let the_next_params = get_direction.next_director.params;
                    next_href = func.url_path(the_next_route+func.unicode_to_string(the_next_params));
                }
            }catch(err){
                next_href = "";
            }
            //
            if(direction_history.length <= 1){
                before_click = "hide";
                next_click = "hide";
            }else{
                //
                if (before_href === "" && next_href === ""){
                    before_click = "hide";
                    next_click = "hide";
                }else{
                    if (before_href === "") {
                        before_click = "hide";
                    }else{
                        before_click = "click";
                    }
                    if (next_href === "") {
                        next_click = "hide";
                    }else {
                        next_click = "click";
                    }
                }
            }
        });
    }
    // <<<<<< 历史记录算法

    // 刷新页面数据
    afterNavigate(() => {
        show_direction();
    });

</script>


<section class="section-nav bg-neutral-100 dark:bg-neutral-800">
    <!--  导航  -->
    <div class="nav-director-div select-none font-text border-radius no-drag">
        <button type="button" class="nav-director-span nav-director-span-left {before_click} border-radius font-blue" title="Before" data-href="{before_href}" onclick={()=>open_href(before_href)}>
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24"><path fill="currentColor" fill-rule="evenodd" d="M15.488 4.43a.75.75 0 0 1 .081 1.058L9.988 12l5.581 6.512a.75.75 0 1 1-1.138.976l-6-7a.75.75 0 0 1 0-.976l6-7a.75.75 0 0 1 1.057-.081" clip-rule="evenodd"/></svg>
        </button>
        <button type="button" class="nav-director-span nav-director-span-right {next_click} border-radius font-blue" title="Next" data-href="{next_href}" onclick={()=>open_href(next_href)}>
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24"><path fill="currentColor" fill-rule="evenodd" d="M8.512 4.43a.75.75 0 0 1 1.057.082l6 7a.75.75 0 0 1 0 .976l-6 7a.75.75 0 0 1-1.138-.976L14.012 12L8.431 5.488a.75.75 0 0 1 .08-1.057" clip-rule="evenodd"/></svg>
        </button>
    </div>
    <!--  标题  -->
    <div class="nav-title-div center select-none font-title pywebview-drag-region can-drag" data-nav_value="{side_tab_data.tab_value}">{side_tab_data.tab_name}</div>

</section>

<style>
    .section-nav {
        position: fixed;
        z-index: 0;
        width: calc(100% - 220px);
        height: 50px;
        top: 0;
        right: 0;
        overflow-x: hidden;
        overflow-y: hidden;
    }

    .nav-director-div{
        position: absolute;
        top: 0;
        left: 0;
        height: 50px;
        line-height: 50px;
        width: 80px;
        z-index: 1;
        overflow: hidden;
        clear: both;
    }
    .nav-director-span{
        height: 40px;
        line-height: 40px;
        width: 40px;
        text-align: center;
        float: left;
        border: 0;
        outline: none;
        margin-top: 5px;
    }
    .nav-director-span > svg{
        float: inherit !important;
        margin-top: 5px;
        margin-left: 10px;
    }
    .nav-title-div{
        height: 50px;
        line-height: 50px;
        overflow: hidden;
        opacity: 0.8;
    }
</style>