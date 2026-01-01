<script lang="ts">
    import func from "../common/func.svelte.js";
    import {afterNavigate} from "$app/navigation";
    import {onMount, onDestroy} from "svelte";
    import config from "../config";
    import {play_audio_data} from "../stores/play_audio.store.svelte";
    import viteConfig from "../../vite.config";


    // 本页面参数
    let route = $state(func.get_route());
    const player_prefix = "play_audio_";
    let myAudio: any; // 播放对象
    let play_error_timeout = $state(0);
    let play_new_timeout = $state(0);
    let play_current_timeout = $state(0);
    let player_init_state = $state(false);
    let player_show_play = $state("show");
    let player_show_stop = $state("hide");
    let player_show_control = $state("hide");
    let play_list_max_len = $state(1000); // 播放列表最大长度
    let song_info_filename = $state("");
    let song_info_filename_marquee = $state("");
    let play_songs_animation = $state("");

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
            that.get_playing().then(the_playing=>{
                if (!the_playing){
                    console.warn("无播放资料（请先 def.fetch_play_list() ）：", the_playing);
                    that.set_playing({}).then(list=>{});
                    return;
                }else {
                    href = the_playing.href;
                    player_show_play = "hide";
                    player_show_stop = "show";
                    player_show_control = "show";
                    song_info_filename = the_playing.filename || 'Null Song'
                    play_songs_animation = "bg-animation";
                    song_info_filename_marquee = "text-marquee";
                    //
                    func.notice("[" + func.get_translate("playing")+"] "+song_info_filename);
                    // 渲染系统音乐通知栏
                    navigator.mediaSession.metadata = new MediaMetadata({
                        title: the_playing.filename || 'Null Song', // 歌名
                        artist: func.get_translate("playing")+"...", // 艺术家
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
            });
        },
        //
        player_init: function(){ // 初始化
            let that = this;
            //
            console.log("Player Init");
            player_init_state = true;
            play_audio_data.play_state = false;

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
            play_audio_data.play_state = false;
            song_info_filename = "";
            play_songs_animation = "";
            song_info_filename_marquee = "";
        },
        play_stop: function(){ // 暂停播放
            let that = this;
            //
            that.get_playing().then(the_playing=>{
                that.play_clear_timer();
                player_show_play = "show";
                player_show_stop = "hide";
                song_info_filename =  the_playing.filename;
                //
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
            that.get_playing().then(the_playing=>{
                that.get_list().then(list=>{
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
                                            that.set_playing(list[0]).then(list=>{resolve(true);}); // 下一个就是第一个
                                        }else{
                                            that.set_playing(list[i+1]).then(list=>{resolve(true);});
                                        }
                                        break;
                                    }
                                    // 不存在就从第一个开始
                                    if (i+1 === list.length){ // 循环完成
                                        that.set_playing(list[0]).then(list=>{resolve(true);});
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
                });
            });
        },
        play_before: function(){ // 上一首
            let that = this;
            //
            that.play_clear_timer();
            that.set_current_time("0");
            navigator.mediaSession.playbackState = 'playing';
            //
            that.get_playing().then(the_playing=>{
                that.get_list().then(list=>{
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
                                            that.set_playing(list[list.length-1]).then(list=>{resolve(true);}); // 上一个就是最后一个
                                        }else{
                                            that.set_playing(list[i-1]).then(list=>{resolve(true);});
                                        }
                                        break;
                                    }
                                    // 不存在就从最后一个开始
                                    if (i+1 === list.length){ // 循环完成
                                        that.set_playing(list[i]).then(list=>{resolve(true);});
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
                });
            });
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
        get_playing: function(): Promise<object>{ // 获取当前播放
            return new Promise(resolve => {
                func.js_call_py_or_go("get_data", {data_key:player_prefix + "playing"}).then(res=>{
                    let the_playing = res.content.data;
                    resolve(the_playing?JSON.parse(decodeURIComponent(the_playing)):null);
                });
            });
        },
        set_playing: function(the_playing = {}): Promise<object>{ // 新增或更新当前播放
            return new Promise(resolve => {
                func.js_call_py_or_go("set_data", {data_key:player_prefix + "playing", data_value:encodeURIComponent(JSON.stringify(the_playing)), data_timeout_s:180*24*3600 }).then(res=>{
                    let the_playing = res.content.data;
                    resolve(the_playing?JSON.parse(decodeURIComponent(the_playing)):null);
                });
            });
        },
        get_list: function(): Promise<object[]>{ // 获取列表，最大1000长度
            return new Promise(resolve => {
                func.js_call_py_or_go("get_data", {data_key:player_prefix + "list" }).then(res=>{
                    let list = res.content.data;
                    resolve((list.length>0)?JSON.parse(decodeURIComponent(list)).slice(0, play_list_max_len):null);
                });
            });

        },
        set_list: function(list_array:object[] = []): Promise<object[]>{ // 新增或更新列表，最大1000长度
            let list = "";
            if (typeof list_array === "object"){
                list = JSON.stringify(list_array.slice(0, play_list_max_len));
            }else{
                list = list_array;
            }
            return new Promise(resolve => {
                func.js_call_py_or_go("set_data", {data_key:player_prefix + "list", data_value:encodeURIComponent(list), data_timeout_s:2*365*24*3600 }).then(res=>{
                    let the_playing = res.content.data;
                    resolve(the_playing?JSON.parse(decodeURIComponent(the_playing)):null);
                });
            });
        },
        //
        get_current_time: function(): string{ // 获取当前播放进度
            return func.get_local_data(player_prefix + "current_time");
        },
        set_current_time: function(current_time = ""): void{ // 设置当前播放进度
            func.set_local_data(player_prefix + "current_time", current_time);
        },
        play_new_list: function(now_audio_files: object[] = []): void{ // 从新列表播放
            let that = this;
            //
            if (now_audio_files.length > 0){
                that.set_current_time("0");
                that.set_playing(now_audio_files[0]).then(the_playing=>{});
                that.set_list(now_audio_files).then(list=>{});
                play_audio_data.play_state = true;
                func.notice(func.get_translate("updated"));
            }else{
                func.notice(func.get_translate("null_content"));
            }
        },
    };


    // 检测$state()值变化
    $effect(() => {
        if (play_audio_data.play_state){
            def.play_start();
        }else {
            // 跳过false情况
        }
    });


    // 刷新页面数据
    afterNavigate(() => {
        // 展示播放按钮
        def.get_playing().then(the_playing=>{
            if (the_playing){ // 有历史
                player_show_control = "show";
                song_info_filename =  the_playing.filename;
            }else{ // 无历史就加载新的
                //
            }
        });
    });


    // 页面装载完成后，只运行一次
    onMount(()=>{
        myAudio = new Audio();
        //
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

<section class="section-player-box select-none border-radius bg-neutral-200 dark:bg-neutral-800 {player_show_control} ">
    <div class="page-player-song_btns">
        <button type="button" class="player-btn font-mini font-blue click " onclick={()=>def.play_before()} title="Before">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="currentColor" d="M14.91 6.71a.996.996 0 0 0-1.41 0L8.91 11.3a.996.996 0 0 0 0 1.41l4.59 4.59a.996.996 0 1 0 1.41-1.41L11.03 12l3.88-3.88c.38-.39.38-1.03 0-1.41"/></svg>
        </button>
        <button type="button" class="player-btn font-mini font-blue click {player_show_play}" onclick={()=>def.play_start()} title="Play">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 48 48"><path fill="currentColor" d="m16.75 8.412l24.417 12.705a3.25 3.25 0 0 1 0 5.766L16.75 39.588A3.25 3.25 0 0 1 12 36.705v-25.41a3.25 3.25 0 0 1 4.549-2.98z"/></svg>
        </button>
        <button type="button" class="player-btn font-mini font-blue click {player_show_stop} {play_songs_animation} " onclick={()=>def.play_stop()} title="Stop">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><rect width="4" height="14" x="6" y="5" fill="currentColor" rx="1"/><rect width="4" height="14" x="14" y="5" fill="currentColor" rx="1"/></svg>
        </button>
        <button type="button" class="player-btn font-mini font-blue click" onclick={()=>def.play_next()} title="Next">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 48 48"><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="4" d="m19 12l12 12l-12 12"/></svg>
        </button>
    </div>
    <div class="page-player-song_name break-ellipsis">
        <div class="page-player-song_name_txt select-text {song_info_filename_marquee}" title="{song_info_filename}">
            {song_info_filename?song_info_filename:"···"}
        </div>
    </div>
</section>


<style>
    .section-player-box{
        position: fixed;
        bottom: 10px;
        right: 15px;
        width: 110px; /* 220 120 */
        height: 40px;
        overflow: hidden;
        /*padding: 5px 5px;*/
        clear: both;
        border-radius: 20px;
        z-index: 200;
        /*宽度缩放动画*/
        transition: width 0.5s ease-in-out;
    }
    .section-player-box:hover{
        width: 220px;
    }
    .page-player-song_name{
        width: calc(220px - 15px - 100px);
        line-height: 30px;
        height: 30px;
        overflow: hidden;
        float: right;
        opacity: 0.8;
        text-align: center;
        border-radius: 20px;
        margin-left: 5px;
        margin-right: 5px;
        margin-top: 5px;
    }
    .page-player-song_btns{
        width: 100px;
        float: right;
        height: 30px;
        margin-top: 5px;
        border-radius: 20px;
        margin-right: 5px;
    }
    .player-btn{
        width: 30px;
        height: 30px;
        border-radius: 30px;
        text-align: center;
        background-color: rgba(160,160,160,0.2);
        float: left;
        margin-right: 5px;
    }
    .player-btn:last-child{
        margin-right: 0;
    }
    .player-btn > svg{
        margin-top: 0;
        margin-left: 3px;
    }

</style>