<script lang="ts">
    import func from "..//common/func.svelte.js";
    import { page } from '$app/state';
    import { afterNavigate, beforeNavigate } from "$app/navigation";
    import config from "../config.js";
    import {browser} from "$app/environment";
    import {onMount} from "svelte";


    // 历史记录算法 >>>>>>
    // 本页面参数
    let href = $state(func.get_href());
    let route = $state(func.get_route());
    let params = $state(func.get_params());
    let time = $state(func.get_time_date("YmdHis"));
    // CSS显示数据
    let before_href = $state('');
    let before_click = $state('director-btn-not_click');
    let next_href = $state('');
    let next_click = $state('director-btn-not_click');
    // 本页面函数：Svelte的HTML组件onXXX=中正确调用：={()=>def.xxx()}
    const def = {
        open_href: function(href="") { // 打开链接
            let that = this;
            //
            if (href.length >= 1){
                func.open_url(href, "_self");
            }else{ // 空
                // console.log("空链接");
            }
        },
        set_direction_history: function(now_director_dict) {  // 设置访问历史
            let that = this;
            // 回到主页删除历史记录
            if (config.sys.home_route === route){
                func.del_local_data("director_urls");
            }
            // 插入新历史
            let the_direction_urls = func.get_local_data("director_urls");
            let the_direction_urls_array: object[] = [];
            if (the_direction_urls) {
                the_direction_urls_array = func.string_to_json(the_direction_urls);
            }
            return new Promise(resolve => {
                if (the_direction_urls_array.length > 0) {
                    let splice_index = [];
                    let new_director_dict:object[] = [];
                    //
                    let now_href = now_director_dict.href;
                    let now_route = now_director_dict.route;
                    let now_params = now_director_dict.params;
                    //
                    function only_route_name(){ // 路由去重
                        return new Promise(resolve2 => {
                            for (let i = 0; i < the_direction_urls_array.length; i++) {
                                let the_href = the_direction_urls_array[i].href;
                                let the_route = the_direction_urls_array[i].route;
                                let the_params = the_direction_urls_array[i].params;
                                // 去重
                                if (now_href === the_href) { // 已存在路由历史，不再继续添加
                                    resolve2(the_direction_urls_array);
                                    break;
                                }
                                // 限制历史长度
                                if (i>500){
                                    resolve2(the_direction_urls_array);
                                    break;
                                }
                                // 加入当前路由
                                if (i === the_direction_urls_array.length - 1) {
                                    the_direction_urls_array.push(now_director_dict);
                                    resolve2(the_direction_urls_array);
                                }
                            }
                        });
                    }
                    //
                    only_route_name().then(_the_direction_urls_array=>{ // 删除路由的子链接
                        for (let i = 0; i < _the_direction_urls_array.length; i++) {
                            let the_href = _the_direction_urls_array[i].href;
                            let the_route = _the_direction_urls_array[i].route;
                            let the_params = _the_direction_urls_array[i].params;
                            // 删除路由子链接
                            if (now_route === the_route && now_params.length===0 && the_params.length>0){ // 跳过
                                // console.log("1=", i, [now_route, the_route, now_params.length, the_params.length]);
                            }else{
                                new_director_dict.push(the_direction_urls_array[i]);
                            }
                            // 加入当前路由
                            if (i === the_direction_urls_array.length - 1) {
                                func.set_local_data("director_urls", func.json_to_string(new_director_dict));
                                resolve(the_direction_urls_array);
                            }
                        }
                    });
                }else{ // 空记录就新增一个
                    func.set_local_data("director_urls", func.json_to_string([now_director_dict]));
                    resolve([now_director_dict]);
                }
            });
        },
        get_direction_history: function(now_director_dict) {  // 在历史记录中找到上一页、下一页
            let that = this;
            //
            let the_before_director_dict = {};
            let the_next_director_dict = {};
            //
            let the_direction_urls = func.get_local_data("director_urls");
            let the_direction_urls_array = [];
            if (the_direction_urls) {
                the_direction_urls_array = func.string_to_json(the_direction_urls);
            }
            if (the_direction_urls_array.length > 0){
                let now_href = now_director_dict.href;
                let now_route = now_director_dict.route;
                let now_params = now_director_dict.params;
                let len = the_direction_urls_array.length;
                //
                for (let i = 0; i < the_direction_urls_array.length; i++){
                    let the_href = the_direction_urls_array[i].href;
                    let the_route = the_direction_urls_array[i].route;
                    let the_params = the_direction_urls_array[i].params;
                    if (now_href === the_href) { // 主路由一样，则删除历史
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
        },
        show_direction: function() { // 展示页面数据
            let that = this;
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
            that.set_direction_history(director_dict).then(direction_history=>{
                func.console_log("set_direction_history=", direction_history);
                //
                let get_direction = that.get_direction_history(director_dict);
                //
                try {
                    if (get_direction.before_director.route) {
                        let the_before_href = get_direction.before_director.href;
                        let the_before_route = get_direction.before_director.route;
                        let the_before_params = get_direction.before_director.params;
                        before_href = func.unicode_to_string(the_before_href);
                    }
                }catch(err){
                    before_href = "";
                }
                //
                try {
                    if (get_direction.next_director.route) {
                        let the_next_href = get_direction.next_director.href;
                        let the_next_route = get_direction.next_director.route;
                        let the_next_params = get_direction.next_director.params;
                        next_href = func.unicode_to_string(the_next_href);
                    }
                }catch(err){
                    next_href = "";
                }
                //
                if(direction_history.length <= 1){
                    before_click = "director-btn-not_click";
                    next_click = "director-btn-not_click";
                }else{
                    //
                    if (before_href === "" && next_href === ""){
                        before_click = "director-btn-not_click";
                        next_click = "director-btn-not_click";
                    }else{
                        if (before_href === "") {
                            before_click = "director-btn-not_click";
                        }else{
                            before_click = "director-btn-click";
                        }
                        if (next_href === "") {
                            next_click = "director-btn-not_click";
                        }else {
                            next_click = "director-btn-click";
                        }
                    }
                }
            });
        }
    };
    // <<<<<< 历史记录算法


    // 刷新页面数据
    afterNavigate(() => {
        def.show_direction(); // 支持goto()链接带参数
    });

    // 页面装载完成后，只运行一次
    onMount(() => {
        //
        def.show_direction(); // 支持goto()链接带参数
    });


</script>

<section class="section-director no-drag">
    <!--  导航  -->
    <div class="director-div select-none font-text">
        <button type="button" class="director-btn director-btn-left {before_click} border-radius font-blue" title="Before" data-href="{before_href}" onclick={()=>def.open_href(before_href)}>
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24"><path fill="currentColor" fill-rule="evenodd" d="M15.488 4.43a.75.75 0 0 1 .081 1.058L9.988 12l5.581 6.512a.75.75 0 1 1-1.138.976l-6-7a.75.75 0 0 1 0-.976l6-7a.75.75 0 0 1 1.057-.081" clip-rule="evenodd"/></svg>
        </button>
        <button type="button" class="director-btn director-btn-right {next_click} border-radius font-blue" title="Next" data-href="{next_href}" onclick={()=>def.open_href(next_href)}>
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24"><path fill="currentColor" fill-rule="evenodd" d="M8.512 4.43a.75.75 0 0 1 1.057.082l6 7a.75.75 0 0 1 0 .976l-6 7a.75.75 0 0 1-1.138-.976L14.012 12L8.431 5.488a.75.75 0 0 1 .08-1.057" clip-rule="evenodd"/></svg>
        </button>
    </div>
</section>

<style>
    .section-director {
        position: fixed;
        z-index: 1;
        width: 80px;
        height: 50px;
        top: 0;
        left: 220px;
        overflow-x: hidden;
        overflow-y: hidden;
    }

    .director-div{
        position: absolute;
        top: 0;
        left: 4px;
        height: 50px;
        line-height: 50px;
        width: 80px;
        z-index: 1;
        overflow: hidden;
        clear: both;
    }
    .director-btn{
        height: 36px;
        line-height: 36px;
        width: 36px;
        text-align: center;
        float: left;
        border: 0;
        outline: none;
        margin-top: 7px;
    }
    .director-btn-click:hover{
        background-color: rgba(180, 180, 180, 0.2);
    }
    .director-btn-click:active{
        background-color: rgba(180, 180, 180, 0.4);
    }
    .director-btn-not_click{
        color: rgba(180, 180, 180, 0.6);
        /*cursor: not-allowed;*/
    }
    .director-btn > svg{
        float: inherit !important;
        margin-left: 8px;
    }
</style>