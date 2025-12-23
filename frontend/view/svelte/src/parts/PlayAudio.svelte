<script lang="ts">
    import func from "../common/func.svelte.js";
    import {afterNavigate} from "$app/navigation";
    import FetchPOST from "../common/post.svelte";
    import {onMount, onDestroy} from "svelte";
    import config from "../config";


    // 本页面参数
    let route = $state(func.get_route());
    const player_prefix = "play_audio_";
    let myAudio = null; // 播放对象
    let play_error_timeout = $state(0);
    let play_new_timeout = $state(0);
    let play_current_timeout = $state(0);
    let player_init_state = $state(false);
    let player_show_play = $state("show");
    let player_show_stop = $state("hide");
    let player_show_control = $state("hide");
    let play_list_max_len = $state(2000); // 播放列表最大长度

    // 用于存储事件监听器引用，便于清理
    let eventListeners = {
        canplaythrough: null,
        loadeddata: null,
        timeupdate: null,
        ended: null,
        error: null
    };


    // 本页面函数：Svelte的HTML组件onXXX=中正确调用：={()=>def.xxx()}
    const def = {
        // 开始播放
        play_start: function(){
            let that = this;
            //
            that.play_clear_timer();
            //
            if ('mediaSession' in navigator) {
                //
            }else{
                console.warn("不支持同步系统播放进度。");
                return;
            }
            // 从本地读取当前音乐
            let href = "";
            let the_playing = that.get_playing();
            if (!the_playing){
                console.warn("无播放资料（请先 def.fetch_play_list() ）：", the_playing);
                that.set_playing("");
                return;
            }else {
                href = the_playing.href;
                player_show_play = "hide";
                player_show_stop = "show";
                // 渲染系统音乐通知栏
                navigator.mediaSession.metadata = new MediaMetadata({
                    title: the_playing.filename || '未知歌曲', // 歌名
                    artist: func.get_translate("playing"), // 艺术家
                    // album: '-', // 专辑
                    artwork: [ // 封面
                        {src: the_playing.cover || '/launcher.png', sizes: '96x96', type: 'image/png'},
                    ]
                });
                navigator.mediaSession.playbackState = 'playing';
            }
            // 从中断的地方继续
            myAudio.src = href;
            myAudio.autoplay = false;
            myAudio.loop = false;
            myAudio.volume = 1; // 音量(0, 1]
            myAudio.currentTime = parseFloat(that.get_current_time()); // 从中断的地方继续播放
            //
            if (!player_init_state){
                that.player_init();
            }
            myAudio.play().catch(err => {
                console.warn("播放失败:", err);
            });
            //
            // 设置操作处理器 - 包括上一曲、下一曲
            try {
                // 上一曲
                navigator.mediaSession.setActionHandler('previoustrack', () => {
                    // console.log('系统上一曲键被点击');
                    that.play_before();
                });
                // 下一曲
                navigator.mediaSession.setActionHandler('nexttrack', () => {
                    // console.log('系统下一曲键被点击');
                    that.play_next();
                });
                // 播放
                navigator.mediaSession.setActionHandler('play', () => {
                    // console.log('系统播放键被点击');
                    that.play_start();
                });
                // 暂停
                navigator.mediaSession.setActionHandler('pause', () => {
                    // console.log('系统暂停键被点击');
                    that.play_stop();
                });

                // 快退
                navigator.mediaSession.setActionHandler('seekbackward', (details) => {
                    // console.log('快退', details);
                    if (myAudio) {
                        const skipTime = details.seekOffset || 5;
                        myAudio.currentTime = Math.max(0, myAudio.currentTime - skipTime);
                        that.set_current_time((myAudio.currentTime - skipTime)+"");
                    }
                });
                // 快进
                navigator.mediaSession.setActionHandler('seekforward', (details) => {
                    // console.log('快进', details);
                    if (myAudio) {
                        const skipTime = details.seekOffset || 5;
                        myAudio.currentTime = Math.min(myAudio.duration, myAudio.currentTime + skipTime);
                        that.set_current_time((myAudio.currentTime + skipTime)+"");
                    }
                });

            } catch (error) {
                console.warn('某些媒体操作不被支持:', error);
            }
        },
        //
        player_init: function(){ // 初始化
            let that = this;
            //
            console.log("Player Init");
            player_init_state = true;

            // 清理旧的事件监听器
            that.cleanup_event_listeners();

            // 创建新的监听器函数（使用命名函数以便移除）
            eventListeners.canplaythrough = function(event) {
                // 音频可以播放；如果权限允许则播放
            };

            eventListeners.loadeddata = function(){ // onload
                console.log("Play Start");
                //
                // 清理旧的timeupdate监听器
                if (eventListeners.timeupdate) {
                    myAudio.removeEventListener('timeupdate', eventListeners.timeupdate);
                }
                // eventListeners.timeupdate = function (e){
                //     let current = myAudio.currentTime; // s
                //     that.set_current_time(current+"");
                //     // console.log("timeupdate=", [myAudio.currentTime, that.get_current_time()]);
                // };
                // myAudio.addEventListener('timeupdate', eventListeners.timeupdate);
                play_current_timeout = setInterval(function(){
                    try {
                        let current = myAudio.currentTime; // s
                        that.set_current_time(current+"");
                    }catch (e) {}
                }, 100); // 最佳范围 [50，150]
            };

            eventListeners.ended = function () { // 播放结束
                console.log("Play Ended");
                that.play_next();
            };

            eventListeners.error = function (){ // error
                console.warn("Play Error");
                play_error_timeout = setTimeout(function () {
                    that.play_next();
                }, 2000);
            };

            // 添加事件监听器
            myAudio.addEventListener('canplaythrough', eventListeners.canplaythrough);
            myAudio.addEventListener("loadeddata", eventListeners.loadeddata);
            myAudio.addEventListener("ended", eventListeners.ended);
            myAudio.onerror = eventListeners.error;
        },

        // 清理事件监听器
        cleanup_event_listeners: function(){
            if (!myAudio) return;

            // 清理事件监听器
            if (eventListeners.canplaythrough) {
                myAudio.removeEventListener('canplaythrough', eventListeners.canplaythrough);
                eventListeners.canplaythrough = null;
            }
            if (eventListeners.loadeddata) {
                myAudio.removeEventListener("loadeddata", eventListeners.loadeddata);
                eventListeners.loadeddata = null;
            }
            if (eventListeners.timeupdate) {
                myAudio.removeEventListener('timeupdate', eventListeners.timeupdate);
                eventListeners.timeupdate = null;
            }
            if (eventListeners.ended) {
                myAudio.removeEventListener("ended", eventListeners.ended);
                eventListeners.ended = null;
            }
            if (eventListeners.error) {
                myAudio.onerror = null;
                eventListeners.error = null;
            }
        },
        //
        play_clear_timer: function(){ // 清除数据，提供初始化环境
            let that = this;
            //
            clearTimeout(play_error_timeout);
            clearTimeout(play_new_timeout);
            clearInterval(play_current_timeout);
            play_error_timeout = 0;
            play_new_timeout = 0;
            play_current_timeout = 0;
        },
        play_stop: function(){ // 暂停播放
            let that = this;
            //
            that.play_clear_timer();
            player_show_play = "show";
            player_show_stop = "hide";
            that.is_playing().then(state=>{
                let current = myAudio.currentTime;
                if (!current){
                    //跳过
                }else{
                    if (state){
                        that.set_current_time(myAudio.currentTime+"");
                    }
                }
                myAudio.pause();
                // 渲染系统音乐通知栏
                let the_playing = that.get_playing();
                navigator.mediaSession.metadata = new MediaMetadata({
                    title: the_playing.filename || '未知歌曲', // 歌名
                    artist: func.get_translate("play_paused"), // 艺术家
                    // album: '-', // 专辑
                    artwork: [ // 封面
                        {src: the_playing.cover || '/launcher.png', sizes: '96x96', type: 'image/png'},
                    ]
                });
                navigator.mediaSession.playbackState = 'paused';
            });
        },
        play_next: function(){ // 下一首
            let that = this;
            //
            that.play_clear_timer();
            that.set_current_time("0");
            // 渲染系统音乐通知栏
            navigator.mediaSession.playbackState = 'playing';
            //
            let the_playing = that.get_playing();
            let list = that.get_list();
            //
            if (the_playing && list){
                let the_href = the_playing.href;
                function calc_playing() {
                    return new Promise(resolve => {
                        for (let i=0; i<list.length; i++){
                            let _the_href = list[i].href;
                            let _the_filename = list[i].filename;
                            let _the_cover = list[i].cover;
                            // 存在
                            if (the_href === _the_href){
                                if (i+1 === list.length){ // 当前是最后一个，
                                    that.set_playing(list[0]); // 下一个就是第一个
                                }else{
                                    that.set_playing(list[i+1]);
                                }
                                resolve(true);
                                break;
                            }
                            // 不存在就从第一个开始
                            if (i+1 === list.length){ // 循环完成
                                that.set_playing(list[0]);
                                resolve(true);
                            }
                        }
                    });
                }
                calc_playing().then(state=>{
                    that.play_start();
                });
            }else{
                console.log("参数不全，1");
            }
        },
        play_before: function(){ // 上一首
            let that = this;
            //
            that.play_clear_timer();
            that.set_current_time("0");
            navigator.mediaSession.playbackState = 'playing';
            //
            let the_playing = that.get_playing();
            let list = that.get_list();
            //
            if (the_playing && list){
                let the_href = the_playing.href;
                function calc_playing() {
                    return new Promise(resolve => {
                        for (let i=0; i<list.length; i++){
                            let _the_href = list[i].href;
                            let _the_filename = list[i].filename;
                            let _the_cover = list[i].cover;
                            // 存在
                            if (the_href === _the_href){
                                if (i === 0){ // 当前是第一个
                                    that.set_playing(list[list.length-1]); // 上一个就是最后一个
                                }else{
                                    that.set_playing(list[i-1]);
                                }
                                resolve(true);
                                break;
                            }
                            // 不存在就从最后一个开始
                            if (i+1 === list.length){ // 循环完成
                                that.set_playing(list[i]);
                                resolve(true);
                            }
                        }
                    });
                }
                navigator.mediaSession.playbackState = 'playing';
                calc_playing().then(state=>{
                    that.play_start();
                });
            }else{
                console.log("参数不全，1");
            }
        },
        //
        is_playing: function(){ // 是否在播放
            let that = this;
            //
            let start_time = that.get_current_time()*1;
            let end_time = 0;
            return new Promise(resolve => {
                setTimeout(function () {
                    end_time = that.get_current_time()*1;
                    resolve(end_time != start_time);
                }, 200);
            });
        },
        //
        set_volume: function(volume = 1){ // 设置音量(0, 1]
            let that = this;
            //
            if (volume < 0 || volume > 1){
                volume = 1;
            }
            myAudio.volume = volume;
        },
        set_playing_loop: function(loop = false){ // 是否循环单个
            let that = this;
            //
            myAudio.loop = loop;
        },
        get_playing_percent: function(){ // 获取当前播放进度
            let that = this;
            //
            let duration = myAudio.duration; // s
            let current = myAudio.currentTime; // s
            return Math.floor((current/duration)*100)/100;
        },
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
        // def.create_player();

    });

    onMount(()=>{
        myAudio = new Audio();
        if (def.get_playing()){ // 有历史
            player_show_control = "show";
        }else{ // 无历史就加载新的
            // route = func.get_route();
            // if (route === "/play_audio"){
            //     def.fetch_play_list().then(_state=>{
            //         if (_state){
            //             player_show_control = "show";
            //         }else{ // 无播放数据
            //             player_show_control = "hide";
            //         }
            //     });
            // }else{
            //     console.log("路由不正确时不加载play_list=", route);
            // }
        }
    });

    onDestroy(()=>{
        // 清理所有定时器
        def.play_clear_timer();

        // 清理所有事件监听器
        def.cleanup_event_listeners();

        // 清理音频对象
        if (myAudio) {
            myAudio.pause();
            myAudio.src = "";
            myAudio = null;
        }

        // 重置状态
        player_init_state = false;
        eventListeners = {
            canplaythrough: null,
            loadeddata: null,
            timeupdate: null,
            ended: null,
            error: null
        };
    });


</script>

<section class="section-play_mp3 select-none border-radius">
    <div class="page-player-div {player_show_control}">
        <button type="button" class="player-btn font-mini font-blue hide" onclick={()=>def.fetch_play_list()} title="Update List">List</button>
        <button type="button" class="player-btn font-mini font-blue hide" onclick={()=>def.play_before()} title="Before">before</button>
        <button type="button" class="player-btn font-mini font-blue {player_show_play}" onclick={()=>def.play_start()} title="Play">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 48 48"><path fill="currentColor" d="m16.75 8.412l24.417 12.705a3.25 3.25 0 0 1 0 5.766L16.75 39.588A3.25 3.25 0 0 1 12 36.705v-25.41a3.25 3.25 0 0 1 4.549-2.98z"/></svg>
        </button>
        <button type="button" class="player-btn font-mini font-blue {player_show_stop}" onclick={()=>def.play_stop()} title="Stop">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><rect width="4" height="14" x="6" y="5" fill="currentColor" rx="1"/><rect width="4" height="14" x="14" y="5" fill="currentColor" rx="1"/></svg>
        </button>
        <button type="button" class="player-btn font-mini font-blue hide" onclick={()=>def.play_next()} title="Next">next</button>
    </div>
</section>


<style>
    .section-play_mp3{
        position: fixed;
        bottom: 10px;
        right: 10px;
        width: 40px;
        height: 40px;
        overflow: hidden;
        padding: 5px 5px;
    }
    .page-player-div{
        width: 100%;
    }
    .player-btn{
        width: 30px;
        height: 30px;
        border-radius: 30px;
        text-align: center;
        background-color: rgba(180,180,180,0.4);
    }
    .player-btn > svg{
        margin-top: 0px;
        margin-left: 3px;
    }
</style>