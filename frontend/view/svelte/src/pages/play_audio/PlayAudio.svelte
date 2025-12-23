<script lang="ts">
    import { resolve } from '$app/paths';
    import { page } from '$app/state';
    import func from "../../common/func.svelte.js";
    import {afterNavigate} from "$app/navigation";
    import {onMount} from "svelte";
    import {Dialog, Portal} from "@skeletonlabs/skeleton-svelte";
    import config from "../../config";
    import FetchPOST from "../../common/post.svelte";

    // 本页面参数
    let route = $state(func.get_route());
    const player_prefix = "play_audio_";
    let play_list_max_len = $state(2000); // 播放列表最大长度

    const animation = 'transition transition-discrete opacity-0 translate-y-[100px] starting:data-[state=open]:opacity-0 starting:data-[state=open]:translate-y-[100px] data-[state=open]:opacity-100 data-[state=open]:translate-y-0';
    // 管理弹窗
    let dir_dialog_is_open = $state(false);


    // 本页面函数：Svelte的HTML组件onXXX=中正确调用：={()=>def.xxx()}
    const def = {
        close_dialog: function(){
            let that = this;
            //
            dir_dialog_is_open = false;
        },
        dir_open_dialog: function(){
            let that = this;
            //
            dir_dialog_is_open = true;
        },
        set_local_dir: function(){ // 设置本地文件夹
            let that = this;
            //
            let data_dict = {
                data_key:"play_audio_dir-1",
                data_value:"/Volumes/文档C（APFS_2025）/软件2025-2/音乐/音乐离线4",
                data_timeout_s: 3600*24*356*20,
            }
            func.js_call_py_or_go("set_data", data_dict).then(res=>{
                console.log(res);
                if (res.state === 1){
                    that.close_dialog();
                }else{
                    console.warn("接口错误：", res);
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
        fetch_play_list: function(){ // 更新播放列表+初始化正在播放的信息
            let that = this;
            /* 参数格式
            * list = [
                  {
                        filename: "",
                        href: "",
                        cover: "",
                  },
              ];
            * */
            //
            let api_url = config.api.api_host+"/api/get_play_audio_list";
            const _app_token = func.get_local_data("app_token");
            const body_dict = {
                app_token: _app_token,
                app_class: config.app.app_class
            };
            return new Promise(resolve => {
                console.log("Update Play List");
                FetchPOST(api_url, body_dict).then(res=>{
                    if (res.state === 1){
                        // console.log("api=", api, res.content.list, typeof res.content.list);
                        let list = res.content.list;
                        if (list.length > 0){
                            that.set_current_time("0");
                            that.set_playing(list[0])
                            that.set_list(list);
                            resolve(true);
                        }else{
                            console.warn("参数仍有错误");
                            resolve(false);
                        }
                    }else{
                        console.log("API有问题=", api_url, res);
                        resolve(false);
                    }
                });
            });
        },
    };


    // 刷新页面数据
    afterNavigate(() => {
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
                Update Play List
            </div>
            <div class="li-group-content select-text">
                <button class="btn btn-sm select-none preset-filled-primary-500 font-text float-left mr-[10px] mb-[10px]" onclick={()=>def.fetch_play_list()}>Update List</button>
            </div>
        </li>

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
                                        <input class="input-style font-text select-text border-radius w-full" type="text" maxlength="2000" placeholder="Input..." value="" />
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
</div>