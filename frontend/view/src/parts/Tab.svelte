<script>
    import func from "../common/func.svelte.js";
    import {afterNavigate} from "$app/navigation";
    import {browser_ok, runtime_ok} from "../services/middleware.svelte.js";
    import config from "../config.js";
    import {browser} from "$app/environment";
    import {onMount} from "svelte";


    // 本页面参数
    let route = $state(func.get_route());
    let tab_data = $state([]);
    const tab_data_array = [ // tab数据，自动适配显示效果
        {
            order: 1, // 排序，数字越小越前面
            icon: '<svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" viewBox="0 0 24 24"><g fill="currentColor"><path d="M10 13v-1.978l1.5-1.094l1.5 1.094V13a.25.25 0 0 1-.25.25h-2.5A.25.25 0 0 1 10 13"/><path d="M3.25 11.5a8.25 8.25 0 1 1 14.578 5.294l2.675 2.676a.75.75 0 0 1-1.06 1.06l-2.678-2.678A8.25 8.25 0 0 1 3.25 11.5m10.942-1.466l-2.25-1.64a.75.75 0 0 0-.884 0l-2.25 1.64a.75.75 0 0 0-.308.606V13c0 .966.784 1.75 1.75 1.75h2.5A1.75 1.75 0 0 0 14.5 13v-2.36a.75.75 0 0 0-.308-.606"/></g></svg>', // 图标，26 px
            title: func.get_translate("PureHome"), // 名字，可视最大8个字母
            route: "/purehome", // 对应的route名字，"/"，"/purehome"
            href: func.url_path("/purehome"), // 跳转地址，"./"，"./purehome"
        },
        {
            order: 3, // 排序，数字越小越前面
            icon: '<svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" viewBox="0 0 24 24"><path fill="currentColor" d="M9.5 21h2.066A4.7 4.7 0 0 1 11 18.75c0-1.025.325-1.974.877-2.75H9.5zM21 9.5v4.833A4.7 4.7 0 0 0 19.25 14H16V9.5zm-6.5 0v4.666a4.7 4.7 0 0 0-.874.334H9.5v-5zM21 8V6.25A3.25 3.25 0 0 0 17.75 3H16v5zm-6.5-5h-5v5h5zM8 3H6.25A3.25 3.25 0 0 0 3 6.25V8h5zM3 9.5v5h5v-5zM3 16v1.75A3.25 3.25 0 0 0 6.25 21H8v-5zm16.25-1a3.75 3.75 0 0 1 .202 7.495l-.199.005v.005a.75.75 0 0 1-.108-1.493l.102-.007l.003-.005a2.25 2.25 0 0 0 .154-4.495l-.154-.005a.75.75 0 0 1-.102-1.493zm-3.5 0a.75.75 0 0 1 .102 1.493l-.102.007a2.25 2.25 0 0 0-.154 4.495l.154.005a.75.75 0 0 1 .102 1.493l-.102.007a3.75 3.75 0 0 1-.2-7.495zm3.5 3a.75.75 0 0 1 .102 1.493l-.102.007h-3.5a.75.75 0 0 1-.102-1.493L15.75 18z"/></svg>',
            title: func.get_translate("Link"), // 名字，可视最大8个字母
            route: "/purehome/link", // 对应的route名字，"/"，"/purehome"
            href: func.url_path("/purehome/link"), // 跳转地址，"./"，"./purehome"
        },
    ];
    const tab_data_array_test = [ // tab数据，自动适配显示效果
        {
            order: 2, // 排序，数字越小越前面
            icon: '<svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" viewBox="0 0 48 48"><g fill="none" stroke="currentColor" stroke-width="4"><path stroke-linecap="round" stroke-linejoin="round" d="M4 44h40"/><ellipse cx="24.5" cy="7" rx="13.5" ry="3"/><path d="M16 9s4.16 8.883 5 15c1.069 7.776-1 20-1 20M32.227 9s-4.16 8.883-5 15C26.157 31.776 28 44 28 44"/></g></svg>', // 图标，26 px
            title: func.get_translate("Divination"), // 名字，可视最大8个字母
            route: "/purehome/divination", // 对应的route名字，"/"，"/purehome"
            href: func.url_path("/purehome/divination"), // 跳转地址，"./"，"./purehome"
        },
    ];
    let tab_div_width = $state(280);
    let tab_item_width = $state(80);
    let glass_div_display = $state("hide");
    let qr_img_display = $state("hide");
    let qr_img_src = $state("");
    let qr_enbig_num = $state(0);
    let qr_enbig_width = $state(20);
    let qr_enbig_height = $state(20);
    let tab_bottom = $state(10);


    // 监听左右滑动
    let touchDo = $state(0);
    let touchStartX = $state(0);
    let touchStartY = $state(0);
    let touchXMin = $state(50); // px
    let touchXMax = $state(260);


    // 本页面函数：Svelte的HTML组件onXXX=中正确调用：={()=>def.xxx()}
    const def = {
        open_url: function (href=""){
            func.open_url(href);
        },
        order_tab_data_array: function (tab_data_array){ // // 根据order大小，从小到大排序，格式 [{order:1}, {order:4}, {order:2}]
            return [...tab_data_array].sort((a, b) => a.order - b.order);
        },
        calc_tab_div_width: function (){ // 计算tab的实际宽度
            let max_screen_width = 300; // px，最小屏幕宽度
            let tab_data_len = tab_data.length; // tab_item数量

            // 留白边框px
            let item_margin = 2;
            let item_padding = 2;
            let auto_item_margin = ((item_padding+item_margin)*2 - item_margin*2*(tab_data_len-1)); // 自适应tab的交叉和

            // tab_item宽度
            if (tab_data_len <= 3){ // tab=[0, 3]
                tab_item_width = 80; // px
            } else { // tab=[4, 8]
                tab_item_width = Math.floor((max_screen_width - auto_item_margin)/tab_data_len);
                if (tab_item_width <= 40){ // tab=8
                    tab_item_width = 40;
                }
            }

            // tab_div总宽
            tab_div_width = tab_item_width*tab_data_len + auto_item_margin;
        },
        route_in_tab_data: function (_route){ // object[]是否含有某key的value值
            return tab_data.find(tab => tab.route === _route);
        },
        swiper_goto_tab: function (director, _route){ // 根据滑动方向，切换到下一个tab的href
            let now_route_index = tab_data.findIndex(item => item.route === _route);
            let next_index = 0;
            let href = "";
            // 获取要goto的href
            if (now_route_index !== -1){
                if (director === "right"){
                    next_index = now_route_index+1;
                    if (next_index<tab_data.length && next_index>=0){
                        href = tab_data[next_index].href;
                    }
                }else if (director === "left"){
                    next_index = now_route_index-1;
                    if (next_index>=0 && next_index<tab_data.length){
                        href = tab_data[next_index].href;
                    }
                }else{
                    console.warn("超方向的swiper=", director);
                }
            }else{
                console.warn("当前路由无对应tab，route=", _route);
            }
            // console.log([now_route_index, next_index, href])
            func.open_url(href);
        },
        is_show_tab: function (){
            if (browser){
                return ( (func.is_desktop() && func.is_firefox()) || func.is_waigo() || func.is_ginthon() );
            }else{
                return false;
            }
        },
        show_glass_div: function (){ // 是否隐藏tab区域
            let that = this;
            //
            if (that.is_show_tab() && that.route_in_tab_data(route)){
                glass_div_display = "show";
            }else{
                glass_div_display = "hide";
            }
        },
        show_qr_div: function (){
            let that = this;
            //
            if (that.route_in_tab_data(route) || route === "/info"  || route === "/purehome/divination"){
                func.make_qr_base64(func.get_href()).then(base64=>{
                    qr_img_display = "show";
                    qr_img_src = base64;
                });
            }else{ // hide
                qr_img_display = "hide";
            }
        },
        qr_enbig: function (){
            if (qr_enbig_num === 0){
                qr_enbig_width = 120;
                qr_enbig_height = 120;
                qr_enbig_num = 1;
            }else{
                qr_enbig_width = 20;
                qr_enbig_height = 20;
                qr_enbig_num = 0;
            }
        },
        watch_touch_swiper: function (id_name) { // 监听左右滑动（PC端Safari不支持，Chrome和Firefox全端支持）
            let that = this;
            //
            if (!browser) {return;}
            //
            const element = document.getElementById(id_name);
            if (!element) {console.warn("id_name=", id_name);return;}

            //
            clearTimeout(touchDo);

            // 关键：设置CSS属性，告诉浏览器如何处理触摸事件
            element.style.touchAction = 'pan-y'; // 允许垂直滚动，但水平滚动由JS处理

            // 或者更严格的：element.style.touchAction = 'none'; // 完全禁止滚动

            element.addEventListener('touchstart', function(e) {
                touchStartX = e.touches[0].clientX;
                touchStartY = e.touches[0].clientY;
            }, { passive: true });

            // 完全移除touchmove监听器，让CSS处理滚动
            // 这样就不会有阻止滚动的尝试了

            element.addEventListener('touchend', function(e) {
                if (!touchStartX) {return;}

                const deltaX = e.changedTouches[0].clientX - touchStartX;
                const deltaY = e.changedTouches[0].clientY - touchStartY;
                const distance = Math.abs(deltaX);

                if (Math.abs(deltaY) < Math.abs(deltaX) / 2 &&
                    distance >= touchXMin && distance <= touchXMax) {
                    // 使用setTimeout或requestAnimationFrame避免阻塞
                    touchDo = setTimeout(() => {
                        if (deltaX > 0) { // right
                            // console.log("right", route);
                            that.swiper_goto_tab("right", route);
                        } else { // left
                            // console.log("left", route);
                            that.swiper_goto_tab("left", route);
                        }
                    }, 0);
                }

                // init
                touchStartX = 0;
                touchStartY = 0;
            }, { passive: true });
        },
        //
    };


    // 刷新页面数据
    afterNavigate(() => {
        if (!func.support_min_js()){return;}
        if (!runtime_ok() || !browser_ok()){return;} // 系统基础条件检测
        // 开始
        route = func.get_route();
        //
        if (func.is_pwa() || func.is_localhost()){
            tab_data = [...tab_data_array, ...tab_data_array_test];
        }else{ // init
            tab_data = tab_data_array;
        }
        tab_data = def.order_tab_data_array(tab_data);
        //
        def.calc_tab_div_width();
        def.show_glass_div();
        def.show_qr_div();
        if (func.is_pwa()){
            tab_bottom = 20;
        }else{
            tab_bottom = 10;
        }
    });


    // 页面装载完成后，只运行一次。
    // addEventListener专用函数
    onMount(() => {
        if (!func.support_min_js()){return;}
        if (!runtime_ok() || !browser_ok()){return;} // 系统基础条件检测
        // 监听左右滑动
        def.watch_touch_swiper("tab-touch_swiper");
    });


</script>

<div class="part-div liquidGlass-div select-none {glass_div_display} " id="tab-touch_swiper">
    <!---->
    <svg style="display: none;">
        <filter id="glass-distortion" x="0%" y="0%" width="100%" height="100%" filterUnits="objectBoundingBox">
            <feturbulence type="fractalNoise" baseFrequency="0.001 0.005" numOctaves="1" seed="17" result="turbulence"></feturbulence>

            <fecomponenttransfer in="turbulence" result="mapped">
                <fefuncr type="gamma" amplitude="1" exponent="10" offset="0.5"></fefuncr>
                <fefuncg type="gamma" amplitude="0" exponent="1" offset="0"></fefuncg>
                <fefuncb type="gamma" amplitude="0" exponent="1" offset="0.5"></fefuncb>
            </fecomponenttransfer>

            <fegaussianblur in="turbulence" stdDeviation="3" result="softMap"></fegaussianblur>

            <fespecularlighting in="softMap" surfaceScale="5" specularConstant="1" specularExponent="100" lighting-color="white" result="specLight">
                <fepointlight x="-200" y="-200" z="300"></fepointlight>
            </fespecularlighting>

            <fecomposite in="specLight" operator="arithmetic" k1="0" k2="1" k3="1" k4="0" result="litImage"></fecomposite>

            <fedisplacementmap in="SourceGraphic" in2="softMap" scale="200" xChannelSelector="R" yChannelSelector="G"></fedisplacementmap>
        </filter>
    </svg>
    <!---->
    <div class="liquidGlass-box pywebview-drag-region can-drag  " id="swiper_tab" style="width: {tab_div_width}px; bottom: {tab_bottom}px;" >
        <div class="liquidGlass-wrapper">
            <div class="liquidGlass-effect"></div>
            <div class="liquidGlass-tint"></div>
            <div class="liquidGlass-shine"></div>
            <div class="liquidGlass-text">
                <!---->
                {#each tab_data as item}
                    <button class="tab-item select-none {(route === item.route)?'tab-item-active':''}" style="width: {tab_item_width}px;" onclick={()=>def.open_url(item.href)} >
                        <div class="tab-item-icon">{@html item.icon.replace('<svg ', '<svg style="display:inline-block;height:26px;width:26px;" ')}</div>
                        <code class="tab-item-icon font-mini">{@html item.title}</code>
                    </button>
                {/each}
                <!---->
                <div class="clear"></div>
            </div>
        </div>
    </div>
</div>

<button class="tab-qr-box select-none font-mini click {qr_img_display} " style="width: {qr_enbig_width}px; height: {qr_enbig_height}px;" onclick={()=>def.qr_enbig()}>
    <img class="tab-qr-img" src="{qr_img_src}" alt="QR" />
</button>

<style>
    /**/
    .liquidGlass-box {
        position: fixed;
        /*bottom: 15px;*/
        left: 0;
        right: 0;
        margin: 0 auto;
        width: calc(270px);
        z-index: 1;
        border-radius: 30px;
    }
    .liquidGlass-wrapper {
        position: relative;
        display: flex;
        overflow: hidden;
        /*box-shadow: 0 0 2px rgba(30, 30, 30, 0.8), 0 0 20px rgba(0, 0, 0, 0);*/
        border: 1px solid rgba(160,160,160, 0.6);
        transition: all 0.1s cubic-bezier(0.175, 0.885, 0.32, 2.2);
        border-radius: 30px;
        padding: 0 5px;
    }
    .liquidGlass-effect {
        position: absolute;
        z-index: 0;
        inset: 0;
        backdrop-filter: blur(4px);
        filter: url(#glass-distortion);
        overflow: hidden;
        isolation: isolate;
        border-radius: 30px;
    }
    .liquidGlass-tint {
        z-index: 1;
        position: absolute;
        inset: 0;
        background: rgba(160,160,160, 0.1);
        border-radius: 30px;
    }
    .liquidGlass-shine {
        position: absolute;
        inset: 0;
        z-index: 2;
        overflow: hidden;
        /*box-shadow: inset 2px 2px 1px 0 rgba(255, 255, 255, 0.2), inset -1px -1px 1px 1px rgba(255, 255, 255, 0.2);*/
        border: 1px solid rgba(250,250,250, 0);
        border-radius: 30px;
    }
    .liquidGlass-text {
        z-index: 3;
        background-color: transparent;
        margin: 3px 0;
    }

    /**/
    .tab-item{
        /*width: 72px; !*80px 72px *!*/
        margin: 0 -2px;
        padding: 2px 0 0 0;
        overflow: hidden;
        text-align: center;
        border: none;
        outline: none;
        float: left;
        border-radius: 25px;
        transition: all 0.1s ease-in;
        opacity: 1;
        cursor: pointer;
        font-weight: 400;
        /*  移除原始点击效果  */
        box-shadow: none;
        background: transparent;
        -webkit-tap-highlight-color: transparent;
    }
    /*.tab-item:hover{*/
    /*    opacity: 0.9;*/
    /*}*/
    /*.tab-item:active{*/
    /*    opacity: 1;*/
    /*}*/
    .tab-item-active{
        /*效果1*/
        /*color: var(--color-blue-500);*/
        /*background-color: rgba(30,144,255, 0.2);*/
        /*效果2*/
        background-color: rgba(42,126,255, 0.5);
        /*效果3*/
        /*color: var(--color-blue-500);*/
        /*background-color: rgba(180,180,180, 0.2);*/
    }
    .tab-item-icon{
        opacity: 0.9;
    }

    /**/
    .tab-qr-box{
        position: fixed;
        z-index: 1;
        right: 12px;
        bottom: 85px;
        padding: 1px 1px;
        background-color: transparent;
        overflow: hidden;
        opacity: 0.9;
    }
    .tab-qr-img{
        width: 100%;
        height: 100%;
        border-radius: 5px;
        border: 1px solid rgba(160,160,160, 1);;
        outline: none;
    }

    code{
        outline: none;
        border: none;
        display: inline-block;
    }



</style>