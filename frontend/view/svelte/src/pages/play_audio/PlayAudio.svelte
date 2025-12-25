<script lang="ts">
    import { resolve } from '$app/paths';
    import { page } from '$app/state';
    import func from "../../common/func.svelte.js";
    import {afterNavigate, goto} from "$app/navigation";
    import {onMount} from "svelte";
    import {Dialog, Portal} from "@skeletonlabs/skeleton-svelte";
    import config from "../../config";
    import FetchPOST from "../../common/post.svelte";
    import {notice_data} from "../../stores/notice.store.svelte";
    import {play_audio_data} from "../../stores/play_audio.store.svelte";

    // 本页面参数
    let route = $state(func.get_route());
    const player_prefix = "play_audio_";
    let play_list_max_len = $state(1000); // 播放列表最大长度

    const animation = 'transition transition-discrete opacity-0 translate-y-[100px] starting:data-[state=open]:opacity-0 starting:data-[state=open]:translate-y-[100px] data-[state=open]:opacity-100 data-[state=open]:translate-y-0';
    const icon_dir = '<svg class="svg-icon font-blue" xmlns="http://www.w3.org/2000/svg" width="24" height="22" viewBox="0 0 24 24"><path fill="currentColor" d="M4 20q-.825 0-1.412-.587T2 18V6q0-.825.588-1.412T4 4h5.175q.4 0 .763.15t.637.425L12 6h8q.825 0 1.413.588T22 8v10q0 .825-.587 1.413T20 20z"/></svg>';
    const icon_audio = '<svg class="svg-icon font-blue" xmlns="http://www.w3.org/2000/svg" width="24" height="22" viewBox="0 0 24 24"><path fill="currentColor" d="M10.75 18.692q.816 0 1.379-.563q.563-.564.563-1.379v-3.98h2.731v-1.54h-3.5v4.087q-.236-.257-.53-.383q-.293-.126-.643-.126q-.815 0-1.379.563q-.563.564-.563 1.379t.563 1.379q.564.563 1.379.563M6.616 21q-.691 0-1.153-.462T5 19.385V4.615q0-.69.463-1.152T6.616 3H14.5L19 7.5v11.885q0 .69-.462 1.153T17.384 21zM14 8h4l-4-4z"/></svg>';
    const icon_video = '<svg class="svg-icon font-blue" xmlns="http://www.w3.org/2000/svg" width="24" height="22" viewBox="0 0 24 24"><path fill="currentColor" d="M22.525 7.149a1 1 0 0 0-.972-.044L19 8.382V8c0-1.654-1.346-3-3-3H5C3.346 5 2 6.346 2 8v8c0 1.654 1.346 3 3 3h11c1.654 0 3-1.346 3-3v-.382l2.553 1.276a.99.99 0 0 0 .972-.043c.295-.183.475-.504.475-.851V8c0-.347-.18-.668-.475-.851M7 13.5a1.5 1.5 0 1 1-.001-2.999A1.5 1.5 0 0 1 7 13.5"/></svg>';
    const icon_type = '<svg class="svg-icon font-blue" xmlns="http://www.w3.org/2000/svg" width="24" height="22" viewBox="0 0 24 24"><path fill="currentColor" d="M14 2.25a.25.25 0 0 1 .25.25v5.647c0 .414.336.75.75.75h4.5a.25.25 0 0 1 .25.25V19A2.75 2.75 0 0 1 17 21.75H7A2.75 2.75 0 0 1 4.25 19V5A2.75 2.75 0 0 1 7 2.25z"/><path fill="currentColor" d="M16.086 2.638c-.143-.115-.336.002-.336.186v4.323c0 .138.112.25.25.25h3.298c.118 0 .192-.124.124-.22L16.408 2.98a1.8 1.8 0 0 0-.322-.342"/></svg>';
    // 管理弹窗
    let dir_dialog_is_open = $state(false);
    let input_value_set_dir = $state("");
    let list_dirs = $state([]);
    let list_files = $state([]);
    let root_paths = $state([]);
    let view_path = $state("");
    let has_paths: unknown = $state([]);
    let show_play_all_btn = $state("hide");
    let now_audio_files = $state([]); // 当前文件白名单


    // 本页面函数：Svelte的HTML组件onXXX=中正确调用：={()=>def.xxx()}
    const def = {
        close_dialog: function(){
            let that = this;
            //
            dir_dialog_is_open = false;
            input_value_set_dir = "";
        },
        dir_open_dialog: function(){
            let that = this;
            //
            dir_dialog_is_open = true;
        },
        make_file_token: function(filepath = ""){
            const _app_token = func.get_local_data("app_token");
            return "file_token="+func.md5("filetoken#@"+filepath)+"&app_token=" + _app_token;
        },
        open_file: function(filename = ""){
            let that = this;
            //
            let file_path = view_path + "/" + filename;
            let href = config.api.api_host + "/dir/play_audio/" + encodeURIComponent(file_path) + "?"+that.make_file_token(file_path)+"&ap=dir ";
            func.open_url_with_default_browser(href);
        },
        has_audio_file: function(files_array = []){
            let that = this;
            //
            show_play_all_btn = "hide";
            //
            for (let i=0; i<files_array.length; i++){
                let the_file = files_array[i];
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
        },
        get_play_audio_list: function(now_dir = ""){ // 获取文件夹和文件的tree结构
            let that = this;
            //
            func.loading_show();
            //
            if (!now_dir){
                now_dir = func.search_param("dir");
            }
            console.log("dir=", now_dir);
            //
            view_path = func.converted_path(now_dir); // 获取正确的路径
            //
            let api_url = config.api.api_host+"/api/get_play_audio_list";
            const _app_token = func.get_local_data("app_token");
            const body_dict = {
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
                        //
                        that.has_audio_file(list_files);
                        if (!now_dir && res.content.root_paths.length > 0){
                            root_paths = res.content.root_paths;
                        }
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
                func.js_call_py_or_go("get_data", {data_key:play_audio_list_dir_key}).then(res=>{
                    console.log("get_data=", res);
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
        set_local_dir: function(){ // 设置本地文件夹
            let that = this;
            //
            let value = input_value_set_dir.trim().replaceAll("#@", "").replaceAll("～", ""); // 删除预设的特殊字符
            // 设置多个dir本地记录
            let play_audio_list_dir_key = "play_audio_list_dirs";
            let play_audio_list_dir = "";
            func.js_call_py_or_go("get_data", {data_key:play_audio_list_dir_key}).then(res=>{
                // console.log("get_data=", res);
                if (res.state === 1){
                    play_audio_list_dir = res.content.data;
                }else{
                    func.notice("无数据或接口错误-1：", res);
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
                        data_key: play_audio_list_dir_key,
                        data_value: new_value,
                        data_timeout_s: 3600*24*356*20,
                    }
                    // console.log("data_dict=", data_dict, [play_audio_list_dir_array, play_audio_list_dir]);
                    func.js_call_py_or_go("set_data", data_dict).then(res2=>{
                        // console.log("set_data=", res2);
                        func.notice(res.msg);
                        if (res.state === 1){
                            that.close_dialog();
                            that.get_play_audio_list(); // 更新数据
                        }else{
                            that.close_dialog();
                            func.notice("无数据或接口错误-2：", res2);
                        }
                    });
                }else{
                    func.notice("输入不能为空：", value);
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
        set_list: function(list_array = []){ // 新增或更新列表，最大1000长度
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
            }else{
                func.notice("空列表");
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
    <ul class="ul-group font-text">

        <li class="li-group select-none">
            <div class="li-group-title break">
                设置本地文件夹
            </div>
            <div class="li-group-content select-text">
                <button class="btn btn-sm select-none preset-filled-primary-500 font-text float-left mr-[10px] mb-[10px]" onclick={()=>def.dir_open_dialog()}>Set Local Dir</button>
                <!--  -->
                <Dialog closeOnInteractOutside={false} closeOnEscape={false} open={dir_dialog_is_open} onOpenChange={()=>{}}>
                    <Portal>
                        <Dialog.Backdrop class="fixed inset-0 z-50 bg-surface-50-950/80  pywebview-drag-region can-drag select-none" />
                        <Dialog.Positioner class="fixed inset-0 z-50 flex justify-center items-center font-text">
                            <Dialog.Content class="card bg-neutral-100 dark:bg-neutral-800 w-full max-w-xs p-4 space-y-4 shadow-xl {animation}  px-[10px] py-[10px] border-radius">
                                <header class="flex justify-between items-center pywebview-drag-region can-drag select-none">
                                    <Dialog.Title class="font-title font-bold">⚠️</Dialog.Title>
                                </header>
                                <Dialog.Description class="font-text">
                                    <label class="label">
                                        <input class="input-style font-text select-text border-radius w-full" type="text" maxlength="2000" placeholder="Input..." bind:value={input_value_set_dir}  />
                                    </label>
                                </Dialog.Description>
                                <footer class="flex justify-center gap-10 select-none  px-[10px] py-[10px]">
                                    <button title="Cancel" class="btn btn-base preset-tonal font-title" onclick={()=>def.close_dialog()}>{func.get_translate("btn_cancel")}</button>
                                    <button title="Save" type="button" class="btn btn-base preset-filled-primary-500 font-title" onclick={()=>def.set_local_dir()}>{func.get_translate("btn_save")}</button>
                                </footer>
                            </Dialog.Content>
                        </Dialog.Positioner>
                    </Portal>
                </Dialog>
            </div>

        </li>
    </ul>

    <div class="list_dirs font-text">
        <div class="list-path">已保存的文件夹：{(has_paths.length>0)?JSON.stringify(has_paths):""}</div>
        <div class="list-path">正在访问文件夹：{view_path?view_path:"/"}</div>
        <div class="list-path hide">{JSON.stringify(list_dirs)}</div>
        <ul class="list-path-tree list-path-dirs">
            <div class="show_play_operation select-none ">
                <span class="{show_play_all_btn}">
                    将当前文件夹全部音乐添加到播放列表
                    <button type="button" class="show_play_all-btn click" onclick={()=>def.play_all()} title="Play All"><svg class="font-blue" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="currentColor" d="M18 9V7h-2V5h2V3h2v2h2v2h-2v2zM6 16h7v-3H6zm0-5h7V8H6zm-2 9q-.825 0-1.412-.587T2 18V6q0-.825.588-1.412T4 4h10.425q-.2.45-.312.963T14 6q0 .85.263 1.613T15 9v7h3v-5.1q.25.05.488.075T19 11q.85 0 1.613-.262T22 10v8q0 .825-.587 1.413T20 20z"/></svg></button>
                </span>
            </div>
            {#each list_dirs as dir}
                <li class="list-path-tree-li">
                    <button class="list-path-tree-li-btn click" type="button" title="{dir}" onclick={()=>func.open_url(func.get_route()+"#dir="+encodeURIComponent(func.converted_path(view_path+"/"+dir)))} >{@html icon_dir} {dir}</button>
                    <span>复制链接</span>
                </li>
            {/each}
        </ul>
        <ul class="list-path-tree list-path-files">
            {#each list_files as filename}
                <li class="list-path-tree-li">
                    <button class="list-path-tree-li-btn click" type="button" title="{filename}" onclick={()=>def.open_file(filename)}>{@html func.is_audio(filename)?icon_audio:(func.is_video(filename)?icon_video:icon_type)} {filename}</button>
                    <span>复制链接</span>
                </li>
            {/each}
        </ul>
    </div>

</div>

<style>
    .list_dirs{
        clear: both;
        width: 100%;
        padding: 10px 0;
    }
    .list-path{
        margin-bottom: 10px;
    }
    .list-path-tree{
        padding: 10px 10px;
    }
    .list-path-tree-li{
        padding: 5px 0;
        line-height: 24px;
        opacity: 0.8;
    }
    .list-path-tree-li-btn{
        padding: 5px 0;
        line-height: 20px;
        text-align: left;
    }
    .show_play_all-btn{
        width: 30px;
        height: 30px;
        border-radius: 30px;
        text-align: center;
        background-color: rgba(180,180,180,0.4);
    }
    .show_play_all-btn > svg{
        margin-top: 0px;
        margin-left: 3px;
    }
    .show_play_operation{
        height: 50px;
        padding: 10px 10px;
    }
</style>