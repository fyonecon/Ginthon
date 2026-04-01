<script lang="ts">
    import { resolve } from '$app/paths';
    import func from "../../common/func.svelte.js";
    import {afterNavigate} from "$app/navigation";
    import {onMount} from "svelte";
    import {browser_ok, runtime_ok} from "../../services/middleware.svelte";
    import {browser} from "$app/environment";

    
    // 本页面参数
    let route = $state(func.get_route());
    let textarea_value = $state("");
    let qr_img_src = $state("");
    let qr_img_show = $state("hide");
    let textarea_ele: HTMLElement | null = $state(null);

    // 本页面函数：Svelte的HTML组件onXXX=中正确调用：={()=>def.xxx()}
    const def = {
        make_qr: function(){
            let _textarea_value = textarea_value.trim();
            if (_textarea_value){
                //
                func.make_qr_base64(_textarea_value, 640, 640).then(base64=>{
                    qr_img_src = base64;
                    //
                    if (qr_img_src.length > 10){
                        qr_img_show = "show";
                    }else{
                        qr_img_show = "hide";
                    }
                });
            }else{
                func.notice(func.get_translate("null_content"), "", 2000);
                qr_img_src = "";
                qr_img_show = "hide";
                textarea_ele?.focus();
            }
        },
    };


    // 页面函数执行的入口，实时更新数据
    function page_start(){
        func.console_log("page_start=", route);
        func.loading_hide(); // 避免其他页面跳转到本页面时出现loading图
        // 开始
        func.title(func.get_translate("make_qr"));
    }

    // 标签处于切换显示状态
    function page_show(){
        func.console_log("page_show=", route);
        // show
    }

    // 标签处于切换隐藏状态
    function page_hide(){
        func.console_log("page_hide=", route);
        // hide
    }


    // 刷新页面数据
    afterNavigate(() => {
        if (!func.support_min_js()){return;}
        if (!runtime_ok() || !browser_ok()){return;} // 系统基础条件检测
        //
        page_start();
    });


    // 页面装载完成后，只运行一次
    // addEventListener专用函数
    onMount(() => {
        if (!func.support_min_js()){return;}
        if (!runtime_ok() || !browser_ok()){return;} // 系统基础条件检测
        // 监测页面标签是否处于显示
        if (browser){
            document.addEventListener("visibilitychange", () => {
                if (document.hidden) { // onHide
                    page_show();
                } else { // onShow
                    page_hide();
                }
            });
        }
    });


</script>

<div class="page-div qr-box select-none">
    <div>
        <div class="qr-title-tip font-title hide">{func.get_translate("text_to_qr_btn")}</div>
        <div class="qr-edit select-none">
            <textarea
                    class="textarea-div scroll-y-style select-text border-radius font-title bg-surface-100 dark:bg-surface-800"
                    placeholder="{func.get_translate('textarea_placeholder')}"
                    bind:this={textarea_ele}
                    bind:value={textarea_value}
                    onmouseenter={(e) => e.currentTarget.focus()}
            ></textarea>
        </div>
        <div class="qr-btn select-none">
            <button class="btn btn-base preset-filled-primary-500 font-text click" type="button" title="OK" onclick={def.make_qr}>{func.get_translate("text_to_qr_btn")}</button>
        </div>
        <div class="qr-show select-none">
            <img class="qr-show-img border-radius font-text {qr_img_show}" src="{qr_img_src}" alt="QR" />
        </div>
    </div>
</div>

<style>
    .qr-box{
        padding: 10px 10px;
    }

    .qr-title-tip{
        margin-bottom: 20px;
    }
    .textarea-div{
        width: 100%;
        height: 150px;
        padding: 10px 10px 20px 10px;
        outline: none;
        border: none;
        resize: none;
    }
    .qr-btn{
        padding: 10px 0;
        text-align: center;
    }
    .qr-show{
        padding: 10px 0;
    }

    .qr-show-img{
        background-color: rgba(160,160,160, 0.2);
        width: 100%;
        height: auto;
        max-height: 1000px;
        outline: none;
        border: 1px solid rgba(160,160,160, 1);
    }

</style>