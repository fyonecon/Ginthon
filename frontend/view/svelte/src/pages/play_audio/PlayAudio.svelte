<script lang="ts">
    import { resolve } from '$app/paths';
    import { page } from '$app/state';
    import func from "../../common/func.svelte.js";
    import {afterNavigate, goto} from "$app/navigation";
    import {onMount} from "svelte";
    import {Dialog, Portal} from "@skeletonlabs/skeleton-svelte";
    import config from "../../config";
    import FetchPOST from "../../common/post.svelte";
    import {play_audio_data} from "../../stores/play_audio.store.svelte";

    // 本页面参数
    let route = $state(func.get_route());
    const player_prefix = "play_audio_";
    let play_list_max_len = $state(1000); // 播放列表最大长度

    const animation = 'transition transition-discrete opacity-0 translate-y-[100px] starting:data-[state=open]:opacity-0 starting:data-[state=open]:translate-y-[100px] data-[state=open]:opacity-100 data-[state=open]:translate-y-0';
    const icon_dir = '<svg class="svg-icon font-blue" xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 24 24"><path fill="currentColor" d="M4 20q-.825 0-1.412-.587T2 18V6q0-.825.588-1.412T4 4h5.175q.4 0 .763.15t.637.425L12 6h8q.825 0 1.413.588T22 8v10q0 .825-.587 1.413T20 20z"/></svg>';
    const icon_audio = '<svg class="svg-icon font-blue" xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 24 24"><path fill="currentColor" d="M10.75 18.692q.816 0 1.379-.563q.563-.564.563-1.379v-3.98h2.731v-1.54h-3.5v4.087q-.236-.257-.53-.383q-.293-.126-.643-.126q-.815 0-1.379.563q-.563.564-.563 1.379t.563 1.379q.564.563 1.379.563M6.616 21q-.691 0-1.153-.462T5 19.385V4.615q0-.69.463-1.152T6.616 3H14.5L19 7.5v11.885q0 .69-.462 1.153T17.384 21zM14 8h4l-4-4z"/></svg>';
    const icon_video = '<svg class="svg-icon font-blue" xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 24 24"><path fill="currentColor" d="M22.525 7.149a1 1 0 0 0-.972-.044L19 8.382V8c0-1.654-1.346-3-3-3H5C3.346 5 2 6.346 2 8v8c0 1.654 1.346 3 3 3h11c1.654 0 3-1.346 3-3v-.382l2.553 1.276a.99.99 0 0 0 .972-.043c.295-.183.475-.504.475-.851V8c0-.347-.18-.668-.475-.851M7 13.5a1.5 1.5 0 1 1-.001-2.999A1.5 1.5 0 0 1 7 13.5"/></svg>';
    const icon_type = '<svg class="svg-icon font-blue" xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 24 24"><path fill="currentColor" d="M14 2.25a.25.25 0 0 1 .25.25v5.647c0 .414.336.75.75.75h4.5a.25.25 0 0 1 .25.25V19A2.75 2.75 0 0 1 17 21.75H7A2.75 2.75 0 0 1 4.25 19V5A2.75 2.75 0 0 1 7 2.25z"/><path fill="currentColor" d="M16.086 2.638c-.143-.115-.336.002-.336.186v4.323c0 .138.112.25.25.25h3.298c.118 0 .192-.124.124-.22L16.408 2.98a1.8 1.8 0 0 0-.322-.342"/></svg>';
    // 管理弹窗
    let add_dir_dialog_is_open = $state(false);
    let update_play_list_dialog_is_open = $state(false);
    let input_value_add_dir = $state("");
    let input_value_find = $state("");
    let list_dirs: string[] = $state([]);
    let list_files: string[] = $state([]);
    let view_path = $state("");
    let now_root_path = $state("");
    let has_paths: unknown = $state([]);
    let show_play_all_btn = $state("hide");
    let show_set_local_dir_btn = $state("show");
    let now_audio_files: object[] = $state([]); // 当前文件白名单
    let input_value_find_list_dirs: string[] = $state([]);
    let input_value_find_list_files: string[] = $state([]);
    let show_dir_remove_btn = $state("hide");
    let remove_local_dir_dialog_is_open = $state(false);
    let remove_local_dir_the_dir = $state("");


    // 本页面函数：Svelte的HTML组件onXXX=中正确调用：={()=>def.xxx()}
    const def = {
        close_dialog: function(){
            let that = this;
            //
            add_dir_dialog_is_open = false;
            update_play_list_dialog_is_open = false;
            input_value_add_dir = "";
            remove_local_dir_the_dir = "";
            remove_local_dir_dialog_is_open = false;
        },
        add_dir_open_dialog: function(){
            let that = this;
            //
            add_dir_dialog_is_open = true;
        },
        update_play_list_open_dialog: function(){
            let that = this;
            //
            update_play_list_dialog_is_open = true;
        },
        remove_local_dir_open_dialog: function(dir = ""){
            let that = this;
            //
            remove_local_dir_dialog_is_open = true;
            remove_local_dir_the_dir = dir;
        },
        make_file_token: function(filepath = ""){
            const _app_token = func.get_local_data("app_token");
            return "file_token="+func.md5("filetoken#@"+filepath)+"&app_token=" + _app_token;
        },
        open_file: function(filename = ""){ // 浏览器打开
            let that = this;
            //
            let file_path = view_path + "/" + filename;
            let href = config.api.api_host + "/dir/play_audio/" + encodeURIComponent(file_path) + "?"+that.make_file_token(file_path)+"&ap=dir ";
            func.open_url_with_default_browser(href);
        },
        open_in_folder: function(filepath = ""){ // 本地打开文件夹/文件
            let that = this;
            //
            func.js_call_py_or_go("open_in_folder", {
                lang: func.get_lang(),
                filepath: filepath
            }).then(res=>{
                // console.log("open_in_folder=", res);
                func.notice(res.msg);
            });
        },
        has_audio_file: function(files_array:string[] = []){
            let that = this;
            //
            show_play_all_btn = "hide";
            try {
                for (let i=0; i<files_array.length; i++){
                    let the_file = files_array[i].name;
                    let file_path = view_path+"/"+the_file;
                    if (func.is_audio(the_file)){
                        show_play_all_btn = "show";
                        let the_file_dict = {
                            filename: the_file,
                            href: config.api.api_host + "/dir/play_audio/" + encodeURIComponent(file_path) + "?"+that.make_file_token(file_path)+"&ap=player ",
                            cover: "",
                        };
                        now_audio_files.push(the_file_dict);
                    }
                }
            }catch (e) {}
        },
        get_play_audio_list: function(now_dir = ""){ // 获取文件夹和文件的tree结构
            let that = this;
            //
            func.loading_show();
            list_dirs = [];
            list_files = [];
            input_value_find_list_dirs = [];
            input_value_find_list_files = [];
            input_value_find = "";
            //
            if (!now_dir){
                now_dir = func.search_param("dir");
            }
            func.console_log("dir=", now_dir);
            //
            view_path = func.converted_path(now_dir); // 获取正确的路径
            //
            let api_url = config.api.api_host+"/api/get_play_audio_list";
            const _app_token = func.get_local_data("app_token");
            const body_dict = {
                lang: func.get_lang(),
                app_token: _app_token,
                app_class: config.app.app_class,
                now_dir: view_path,
            };
            return new Promise(resolve => {
                console.log("Update Play List");
                FetchPOST(api_url, body_dict).then(res=>{
                    func.loading_hide();
                    //
                    if (res.state === 1){
                        list_dirs = res.content.list_dirs;
                        list_files = res.content.list_files;
                        view_path = res.content.view_path;
                        now_root_path = res.content.root_path;
                        //
                        that.has_audio_file(list_files);
                        //
                        if (!now_dir){
                            show_dir_remove_btn = "show";
                        }else{
                            show_dir_remove_btn = "hide";
                        }
                        //
                        resolve(true);
                    }else{
                        console.log("API有问题=", api_url, res);
                        resolve(false);
                    }
                });
            });
        },
        get_local_dir: function(){ // 获取数据记录
            let that = this;
            // 设置多个dir本地记录
            let play_audio_list_dir_key = "play_audio_list_dirs";
            let play_audio_list_dir = "";
            return new Promise(resolve => {
                func.js_call_py_or_go("get_data", {
                    lang: func.get_lang(),
                    data_key:play_audio_list_dir_key
                }).then(res=>{
                    // console.log("get_data=", res);
                    if (res.state === 1){
                        play_audio_list_dir = res.content.data;
                    }
                    // 获取老数据
                    let play_audio_list_dir_array = play_audio_list_dir.split("#@");
                    // console.log("play_audio_list_dir_array=", play_audio_list_dir_array, play_audio_list_dir);
                    if (play_audio_list_dir && play_audio_list_dir_array.length > 0){
                        play_audio_list_dir_array;
                        resolve(play_audio_list_dir_array);
                    }else{
                        resolve([]);
                    }
                });
            });
        },
        remove_local_dir: function(the_root_dir = ""){
            let that = this;
            //
            func.loading_show();
            //
            let value = the_root_dir.trim().replaceAll("#@", "").replaceAll("～", ""); // 删除预设的特殊字符
            // 设置多个dir本地记录
            let play_audio_list_dir_key = "play_audio_list_dirs";
            let play_audio_list_dir = "";
            func.js_call_py_or_go("get_data", {
                lang: func.get_lang(),
                data_key:play_audio_list_dir_key
            }).then(res=>{
                if (res.state === 1){
                    play_audio_list_dir = res.content.data;
                }else{
                    console.log(func.get_translate("error") + ", 1", res);
                }
                // 获取老数据
                let play_audio_list_dir_array = play_audio_list_dir.split("#@");
                let new_value = "";
                if (value){
                    if (play_audio_list_dir && play_audio_list_dir_array.length>=2){
                        new_value = play_audio_list_dir
                            .replaceAll("#@"+value, "")
                            .replaceAll(value + "#@", "")
                            .replaceAll(value, "")
                        ;
                    }else{ // 剩下<=1时，删除所有记录
                        new_value = "";
                    }
                    //
                    let data_dict = {
                        lang: func.get_lang(),
                        data_key: play_audio_list_dir_key,
                        data_value: new_value,
                        data_timeout_s: 3600*24*356*20,
                    }
                    //
                    if (new_value){ // 更新新数据
                        func.js_call_py_or_go("set_data", data_dict).then(res2=>{
                            func.notice(res2.msg);
                            if (res2.state === 1){
                                that.close_dialog();
                                that.get_play_audio_list(); // 更新数据
                            }else{
                                func.loading_hide();
                                that.close_dialog();
                                console.log(func.get_translate("error") + ", 3-1", res2);
                            }
                        });
                    }else{ // 删除数据
                        func.js_call_py_or_go("del_data", data_dict).then(res2=>{
                            func.notice(res2.msg);
                            if (res2.state === 1){
                                that.close_dialog();
                                that.get_play_audio_list(); // 更新数据
                            }else{
                                func.loading_hide();
                                that.close_dialog();
                                console.log(func.get_translate("error") + ", 3-2", res2);
                            }
                        });
                    }
                }else{
                    func.loading_hide();
                    func.notice(func.get_translate("input_null"), value);
                }
            });
        },
        set_local_dir: function(){ // 设置本地文件夹
            let that = this;
            //
            func.loading_show();
            //
            let value = input_value_add_dir.trim().replaceAll("#@", "").replaceAll("～", ""); // 删除预设的特殊字符
            // 设置多个dir本地记录
            let play_audio_list_dir_key = "play_audio_list_dirs";
            let play_audio_list_dir = "";
            func.js_call_py_or_go("get_data", {
                lang: func.get_lang(),
                data_key:play_audio_list_dir_key
            }).then(res=>{
                // console.log("get_data=", res);
                if (res.state === 1){
                    play_audio_list_dir = res.content.data;
                }else{
                    console.log(func.get_translate("error") + ", 1", res);
                }
                // 获取老数据
                let play_audio_list_dir_array = play_audio_list_dir.split("#@");
                let new_value = "";
                if (value){
                    if (play_audio_list_dir && play_audio_list_dir_array.length>0){
                        new_value = play_audio_list_dir + "#@" + value;
                    }else{
                        new_value = value;
                    }
                    // 更新新数据
                    let data_dict = {
                        lang: func.get_lang(),
                        data_key: play_audio_list_dir_key,
                        data_value: new_value,
                        data_timeout_s: 3600*24*356*20,
                    }
                    func.js_call_py_or_go("set_data", data_dict).then(res2=>{
                        func.notice(res2.msg);
                        if (res2.state === 1){
                            that.close_dialog();
                            that.get_play_audio_list(); // 更新数据
                        }else{
                            that.close_dialog();
                            func.loading_hide();
                            console.log(func.get_translate("error") + ", 2-1", res2);
                        }
                    });
                }else{
                    func.loading_hide();
                    func.notice(func.get_translate("input_null"), value);
                }
            });
        },

        //
        get_playing: function(){ // 获取当前播放
            let the_playing = func.get_local_data(player_prefix + "playing");
            return the_playing?JSON.parse(decodeURIComponent(the_playing)):null;
        },
        set_playing: function(the_playing = {}){ // 新增或更新当前播放
            return func.set_local_data(player_prefix + "playing", encodeURIComponent(JSON.stringify(the_playing)));
        },
        get_list: function(){ // 获取列表，最大1000长度
            let list = func.get_local_data(player_prefix + "list");
            return (list.length>0)?JSON.parse(decodeURIComponent(list)).slice(0, play_list_max_len):null;
        },
        set_list: function(list_array:object[] = []){ // 新增或更新列表，最大1000长度
            let list = "";
            if (typeof list_array === "object"){
                list = JSON.stringify(list_array.slice(0, play_list_max_len));
            }else{
                list = list_array;
            }
            func.set_local_data(player_prefix + "list", encodeURIComponent(list));
        },
        get_current_time: function(){ // 获取当前播放进度
            return func.get_local_data(player_prefix + "current_time");
        },
        set_current_time: function(current_time = ""){ // 设置当前播放进度
            func.set_local_data(player_prefix + "current_time", current_time);
        },
        //
        play_all: function(){
            let that = this;
            //
            if (now_audio_files.length > 0){
                that.set_current_time("0");
                that.set_playing(now_audio_files[0]);
                that.set_list(now_audio_files);
                play_audio_data.play_state = true;
                func.notice(func.get_translate("updated"));
            }else{
                func.notice(func.get_translate("null_content"));
            }
            that.close_dialog();
        },
        //
        input_find: function(){
            let that = this;
            //
            if (input_value_find){
                // 缓存数据
                if (input_value_find_list_dirs.length === 0){
                    input_value_find_list_dirs = list_dirs;
                }
                if (input_value_find_list_files.length === 0){
                    input_value_find_list_files = list_files;
                }
                // 初始数据
                list_dirs = [];
                list_files = [];
                let _list_dirs = [];
                let _list_files = [];
                // 重新显示数据
                for (const key in input_value_find_list_dirs){
                    let the_dir = input_value_find_list_dirs[key];
                    if (the_dir.name.toLowerCase().indexOf(input_value_find.toLowerCase()) !== -1){
                        list_dirs.push(the_dir);
                        _list_dirs.push(the_dir);
                    }
                }
                for (const key in input_value_find_list_files) {
                     let the_file = input_value_find_list_files[key];
                     if (the_file.name.toLowerCase().indexOf(input_value_find.toLowerCase()) !== -1){
                        list_files.push(the_file);
                         _list_files.push(the_file);
                     }
                }
                // 重新生成播放列表
                setTimeout(function (){
                    that.has_audio_file(_list_files);
                }, 200);
            }else {
                func.notice(func.get_translate("input_null"));
                // 还原缓存数据
                if (input_value_find_list_dirs.length > 0){
                    list_dirs = input_value_find_list_dirs;
                    input_value_find_list_dirs = [];
                }
                if (input_value_find_list_files.length > 0){
                    list_files = input_value_find_list_files;
                    input_value_find_list_files = [];
                }
            }
        },
        input_enter: function(event){
            let that = this;
            //
            if (event.key === 'Enter') {
                // console.log('Enter pressed:', input_value_find);
                // 执行回车操作
                that.input_find();
            }
        },
    };


    // 刷新页面数据
    afterNavigate(() => {
        def.get_local_dir().then(array=>{
            has_paths = array;
        });
        def.get_play_audio_list();
        //
    });

    // 页面装载完成后，只运行一次
    onMount(() => {
        //
    });


</script>

<div>
    <!--  文件列表  -->
    <div class="list_dirs font-text border-radius">
        <!---->
        <div class="list_dirs-title pywebview-drag-region can-drag break-ellipsis bg-neutral-200 dark:bg-neutral-800">
            {view_path?"/.../ "+view_path.replace(func.replaceLast(now_root_path, func.filepath_to_filename(now_root_path), ""), "")+" /":"/"}
        </div>
        <!---->
        <div class="list_dirs-operation">
            <!---->
            <div class="list_dirs-operation-search">
                <label>
                    <input class="input-style select-text list_dirs-operation-search-input border-radius  font-text" type="text" maxlength="100" placeholder="{func.get_translate('input_placeholder_find')}" bind:value={input_value_find} onkeydown={(event)=>def.input_enter(event)} onmouseenter={(e) => e.currentTarget.focus()} />
                    <button class="list_dirs-operation-search-btn font-white border-radius click  font-mini" type="button" title="Find" onclick={()=>def.input_find()}>{func.get_translate("find_btn")}</button>
                </label>
            </div>
            <!---->
            <div class="list_dirs-operation-do">
                <div class="list_dirs-operation-do-item {show_set_local_dir_btn}">
                    <button type="button" class="operation-do-btn click bg-neutral-200 dark:bg-neutral-800" onclick={()=>def.add_dir_open_dialog()} title="{func.get_translate('play_add_new_fir')}">
                        <svg class="font-blue" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 2048 2048"><path fill="currentColor" d="M1088 960h320v128h-320v320H960v-320H640V960h320V640h128zm-64-832q124 0 238 32t214 90t181 140t140 181t91 214t32 239t-32 238t-90 214t-140 181t-181 140t-214 91t-239 32t-238-32t-214-90t-181-140t-140-181t-91-214t-32-239t32-238t90-214t140-181t181-140t214-91t239-32m0 1664q106 0 204-27t183-78t156-120t120-155t77-184t28-204t-27-204t-78-183t-120-156t-155-120t-184-77t-204-28t-204 27t-183 78t-156 120t-120 155t-77 184t-28 204t27 204t78 183t120 156t155 120t184 77t204 28"/></svg>
                    </button>
                </div>
                <div class="list_dirs-operation-do-item {show_play_all_btn}">
                    <button type="button" class="operation-do-btn click bg-neutral-200 dark:bg-neutral-800" onclick={()=>def.update_play_list_open_dialog()} title="{func.get_translate('play_update_play_list')}">
                        <svg class="font-blue" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="currentColor" d="M7 3h10a1 1 0 0 0 0-2H7a1 1 0 0 0 0 2M0 2a2 2 0 1 0 4 0a2 2 0 1 0-4 0m6 6a1 1 0 0 0 1 1h10a1 1 0 0 0 0-2H7a1 1 0 0 0-1 1M0 8a2 2 0 1 0 4 0a2 2 0 1 0-4 0m10 5H7a1 1 0 0 0 0 2h3a1 1 0 0 0 0-2M0 14a2 2 0 1 0 4 0a2 2 0 1 0-4 0m24 5.55v-6.84a2 2 0 0 0-2.37-2l-6 1.12a2 2 0 0 0-1.63 2v4.93a.27.27 0 0 1-.08.19a.26.26 0 0 1-.19.06h-.23a2.6 2.6 0 0 0-1 .21a2.5 2.5 0 0 0 1 4.79a2.4 2.4 0 0 0 .75-.12A2.49 2.49 0 0 0 16 21.55v-7.31a.5.5 0 0 1 .41-.49l5-.93a.5.5 0 0 1 .59.49v3.45a.27.27 0 0 1-.08.19a.26.26 0 0 1-.19.06h-.23a2.6 2.6 0 0 0-1 .21a2.5 2.5 0 0 0 1 4.79a2.4 2.4 0 0 0 .75-.12A2.49 2.49 0 0 0 24 19.55"/></svg>
                    </button>
                </div>
            </div>
        </div>
        <!---->
        <ul class="list-path-tree-ul">
            <!--dirs-->
            {#each list_dirs as the_dir_info}
                <li class="list-path-tree-li list-path-tree-li-dir border-radius">
                    <div class="list-path-tree-li-icon">
                        {@html icon_dir}
                    </div>
                    <div class="list-path-tree-li-content">
                        <!---->
                        <div class="li-name font-text break">
                            <button class="list-path-tree-li-btn click break select-text" type="button" title="{the_dir_info.name}" onclick={()=>func.open_url(func.get_route()+"?dir="+encodeURIComponent(func.converted_path(view_path+"/"+the_dir_info.name)))} >{the_dir_info.name}</button>
                        </div>
                        <!---->
                        <div class="li-info font-text select-text">
                            <div class="li-info-item font-mini break-ellipsis" title="Folder Size">
                                {the_dir_info.size?the_dir_info.size:""}
                            </div>
                            <div class="li-info-item font-mini break-ellipsis" title="Create time">
                                {the_dir_info.create_time?the_dir_info.create_time:"-"}
                            </div>
                        </div>
                        <!---->
                        <div class="li-operation font-text">
                            <div class="li-operation-item {show_dir_remove_btn}">
                                <button type="button" title="{func.get_translate('remove')}" class="li-operation-item-btn click" onclick={()=>def.remove_local_dir_open_dialog(func.converted_path(view_path+"/"+the_dir_info.name))}>
                                    <svg class="font-red" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M7.5 12h9"/></g></svg>
                                </button>
                            </div>
                            <div class="li-operation-item">
                                <button type="button" title="Open in folder" class="li-operation-item-btn click" onclick={()=>def.open_in_folder(func.converted_path(view_path+"/"+the_dir_info.name))} >
                                    <svg class="font-blue" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="currentColor" fill-rule="evenodd" d="M2.07 5.258C2 5.626 2 6.068 2 6.95V14c0 3.771 0 5.657 1.172 6.828S6.229 22 10 22h4c3.771 0 5.657 0 6.828-1.172S22 17.771 22 14v-2.202c0-2.632 0-3.949-.77-4.804a3 3 0 0 0-.224-.225C20.151 6 18.834 6 16.202 6h-.374c-1.153 0-1.73 0-2.268-.153a4 4 0 0 1-.848-.352C12.224 5.224 11.816 4.815 11 4l-.55-.55c-.274-.274-.41-.41-.554-.53a4 4 0 0 0-2.18-.903C7.53 2 7.336 2 6.95 2c-.883 0-1.324 0-1.692.07A4 4 0 0 0 2.07 5.257M12.25 10a.75.75 0 0 1 .75-.75h5a.75.75 0 0 1 0 1.5h-5a.75.75 0 0 1-.75-.75" clip-rule="evenodd"/></svg>
                                </button>
                            </div>
                        </div>
                    </div>
                </li>
            {/each}
            <!--files-->
            {#each list_files as the_file_info}
                <li class="list-path-tree-li list-path-tree-li-file border-radius">
                    <!---->
                    <div class="list-path-tree-li-icon">
                        {@html func.is_audio(the_file_info.name)?icon_audio:(func.is_video(the_file_info.name)?icon_video:icon_type)}
                    </div>
                    <!---->
                    <div class="list-path-tree-li-content">
                        <!---->
                        <div class="li-name font-text break">
                            <button class="list-path-tree-li-btn click break select-text" type="button" title="{the_file_info.name}" onclick={()=>def.open_file(the_file_info.name)}>{the_file_info.name}</button>
                        </div>
                        <!---->
                        <div class="li-info font-text select-text">
                            <div class="li-info-item font-mini break-ellipsis" title="File Size">
                                {the_file_info.size?the_file_info.size:""}
                            </div>
                            <div class="li-info-item font-mini break-ellipsis" title="Create time">
                                {the_file_info.create_time?the_file_info.create_time:"-"}
                            </div>
                        </div>
                        <!---->
                        <div class="li-operation font-text">
                            <div class="li-operation-item hide">
                                <button type="button" title="Open in folder" class="li-operation-item-btn click" onclick={()=>def.open_in_folder(func.converted_path(view_path+"/"+the_file_info.name))} >
                                    <svg class="font-blue" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="currentColor" fill-rule="evenodd" d="M2.07 5.258C2 5.626 2 6.068 2 6.95V14c0 3.771 0 5.657 1.172 6.828S6.229 22 10 22h4c3.771 0 5.657 0 6.828-1.172S22 17.771 22 14v-2.202c0-2.632 0-3.949-.77-4.804a3 3 0 0 0-.224-.225C20.151 6 18.834 6 16.202 6h-.374c-1.153 0-1.73 0-2.268-.153a4 4 0 0 1-.848-.352C12.224 5.224 11.816 4.815 11 4l-.55-.55c-.274-.274-.41-.41-.554-.53a4 4 0 0 0-2.18-.903C7.53 2 7.336 2 6.95 2c-.883 0-1.324 0-1.692.07A4 4 0 0 0 2.07 5.257M12.25 10a.75.75 0 0 1 .75-.75h5a.75.75 0 0 1 0 1.5h-5a.75.75 0 0 1-.75-.75" clip-rule="evenodd"/></svg>
                                </button>
                            </div>
                        </div>
                    </div>
                </li>
            {/each}
        </ul>
    </div>

</div>

<!-- 新增文件夹 -->
<Dialog closeOnInteractOutside={false} closeOnEscape={false} open={add_dir_dialog_is_open} onOpenChange={()=>{}}>
    <Portal>
        <Dialog.Backdrop class="fixed inset-0 z-50 bg-surface-50-950/80 select-none"/>
        <Dialog.Positioner class="fixed inset-0 z-50 flex justify-center items-center font-text select-none">
            <Dialog.Content
                    class="card bg-neutral-100 dark:bg-neutral-800 w-full max-w-xs p-4 space-y-4 shadow-xl {animation}  px-[10px] py-[10px] border-radius">
                <header class="flex justify-between items-center pywebview-drag-region can-drag">
                    <Dialog.Title class="font-title font-bold">⚠️</Dialog.Title>
                </header>
                <Dialog.Description class="font-text select-text">
                    <div class="font-text" style="margin-top: 10px; margin-bottom: 20px;opacity: 0.8;">
                        {func.get_translate('play_add_new_fir')}
                    </div>
                    <label class="label">
                        <input class="input-style font-text select-text border-radius w-full" type="text"
                               maxlength="2000" placeholder="{func.get_translate('input_placeholder_add_dir')}" bind:value={input_value_add_dir}/>
                    </label>
                </Dialog.Description>
                <footer class="flex justify-center gap-10 select-none  px-[10px] py-[10px]">
                    <button title="Cancel" class="btn btn-base preset-tonal font-title"
                            onclick={()=>def.close_dialog()}>{func.get_translate("btn_cancel")}</button>
                    <button title="Save" type="button" class="btn btn-base preset-filled-primary-500 font-title"
                            onclick={()=>def.set_local_dir()}>{func.get_translate("btn_save")}</button>
                </footer>
            </Dialog.Content>
        </Dialog.Positioner>
    </Portal>
</Dialog>

<!-- 更新播放列表 -->
<Dialog closeOnInteractOutside={false} closeOnEscape={false} open={update_play_list_dialog_is_open} onOpenChange={()=>{}}>
    <Portal>
        <Dialog.Backdrop class="fixed inset-0 z-50 bg-surface-50-950/80 select-none" />
        <Dialog.Positioner class="fixed inset-0 z-50 flex justify-center items-center font-text select-none">
            <Dialog.Content class="card bg-neutral-100 dark:bg-neutral-800 w-full max-w-xs p-4 space-y-4 shadow-xl {animation}  px-[10px] py-[10px] border-radius">
                <header class="flex justify-between items-center pywebview-drag-region can-drag">
                    <Dialog.Title class="font-title font-bold">⚠️</Dialog.Title>
                </header>
                <Dialog.Description class="font-text select-text">
                    {func.get_translate('play_update_play_list')}
                </Dialog.Description>
                <footer class="flex justify-center gap-10 select-none  px-[10px] py-[10px]">
                    <button title="Cancel" class="btn btn-base preset-tonal font-title" onclick={()=>def.close_dialog()}>{func.get_translate("btn_cancel")}</button>
                    <button title="Update" type="button" class="btn btn-base preset-filled-primary-500 font-title" onclick={()=>def.play_all()}>{func.get_translate("btn_update")}</button>
                </footer>
            </Dialog.Content>
        </Dialog.Positioner>
    </Portal>
</Dialog>

<!-- 删除已设置的本地文件夹 -->
<Dialog closeOnInteractOutside={false} closeOnEscape={false} open={remove_local_dir_dialog_is_open} onOpenChange={()=>{}}>
    <Portal>
        <Dialog.Backdrop class="fixed inset-0 z-50 bg-surface-50-950/80  select-none" />
        <Dialog.Positioner class="fixed inset-0 z-50 flex justify-center items-center font-text select-none">
            <Dialog.Content class="card bg-neutral-100 dark:bg-neutral-800 w-full max-w-xs p-4 space-y-4 shadow-xl {animation}  px-[10px] py-[10px] border-radius">
                <header class="flex justify-between items-center pywebview-drag-region can-drag">
                    <Dialog.Title class="font-title font-bold">⚠️</Dialog.Title>
                </header>
                <Dialog.Description class="font-text select-text">
                    {@html func.get_translate('remove_help_1') +":<br/>"+ func.filepath_to_filename(remove_local_dir_the_dir)}
                </Dialog.Description>
                <footer class="flex justify-center gap-10 select-none  px-[10px] py-[10px]">
                    <button title="Cancel" class="btn btn-base preset-tonal font-title" onclick={()=>def.close_dialog()}>{func.get_translate("btn_cancel")}</button>
                    <button title="Update" type="button" class="btn btn-base preset-filled-primary-500 font-title" onclick={()=>def.remove_local_dir(remove_local_dir_the_dir)}>{func.get_translate("remove")}</button>
                </footer>
            </Dialog.Content>
        </Dialog.Positioner>
    </Portal>
</Dialog>

<style>
    .list_dirs{
        clear: both;
        width: calc(100% - 20px);
        border: 1px solid rgba(160,160,160, 0.3);
        margin-left: 10px;
        margin-right: 10px;
    }


    .list_dirs-title{
        height: 50px;
        line-height: 30px;
        overflow: hidden;
        padding: 10px 10px;
        opacity: 0.8;
        clear: both;
    }


    .list_dirs-operation{
        height: 50px;
        padding: 5px 5px;
        clear: both;
        border-bottom: 1px solid rgba(160,160,160,0.3);
    }
    .list_dirs-operation-search{
        width: 240px;
        height: 40px;
        float: left;
        overflow: hidden;
    }
    .list_dirs-operation-do{
        width: calc(100% - 240px);
        height: 40px;
        float: left;
        overflow: hidden;
        padding-left: 10px;
    }
    .list_dirs-operation-search-input {
        float: left;
        height: 34px;
        width: calc(100% - 80px - 10px);
        margin: 3px 5px 3px 2px;
    }
    .list_dirs-operation-search-btn{
        float: left;
        width: 80px;
        margin: 3px 0 3px 2px;
        line-height: 34px;
        background-color: var(--color-primary-400);
    }
    .list_dirs-operation-do-item{
        height: 40px;
        padding: 5px 5px;
        float: right;
    }


    .list-path-tree-ul{
        clear: both;
        padding: 10px 10px 10px 10px;
    }
    .list-path-tree-li{
        opacity: 0.8;
        overflow: hidden;
        /*border-bottom: 1px solid rgba(160,160,160,0.2);*/
        clear: both;
    }
    .list-path-tree-li:nth-child(odd){
        background-color: rgba(160,160,160,0);
    }
    .list-path-tree-li:nth-child(even){
        background-color: rgba(160,160,160,0.1);
    }
    .list-path-tree-li:hover{
        background-color: rgba(160,160,160,0.2);
    }
    /*.list-path-tree-li:last-child{*/
    /*    border-bottom: 1px solid rgba(160,160,160,0);*/
    /*}*/


    .list-path-tree-li-icon{
        width: 35px;
        height: 40px;
        padding-top: 5px;
        float: left;
    }
    .list-path-tree-li-content{
        width: calc(100% - 40px);
        padding: 5px 0;
        float: left;
    }
    .list-path-tree-li-btn{
        text-align: left;
        padding: 5px 5px;
        overflow: hidden;
        line-height: 20px;
        max-height: 68px;
    }


    .li-name{
        float: left;
        width: calc(100% - 90px - 240px);
        overflow: hidden;
    }
    .li-info{
        float: left;
        width: 240px;
        overflow: hidden;
    }
    .li-operation{
        float: right;
        width: 90px; /*edit del share qr (30)*3=90 */
        overflow: hidden;
        line-height: 30px;
    }


    .operation-do-btn{
        width: 30px;
        height: 30px;
        border-radius: 30px;
        text-align: center;
    }
    .operation-do-btn > svg{
        margin-top: 0;
        margin-left: 3px;
    }


    .li-info-item{
        width: 120px;
        height: 30px;
        line-height: 30px;
        text-align: center;
        float: left;
    }
    .li-operation-item{
        width: 30px;
        height: 30px;
        line-height: 30px;
        border-radius: 30px;
        text-align: center;
        float: right;
    }
    .li-operation-item-btn > svg{
        margin-top: 3px;
        margin-left: 5px;
    }


</style>