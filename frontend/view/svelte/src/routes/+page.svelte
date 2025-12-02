
<!--<script>-->
<!--    import Home from './home/+page.svelte';-->
<!--</script>-->

<!--<Home />-->

<script>
    import { redirect } from "@sveltejs/kit";
    import { goto } from '$app/navigation';
    import { page } from '$app/stores';


    // 链接参数
    const url_pathname = $page.url.pathname;
    const url_param = $page.url.search;


    // 重新定向到默认页面
    try {
        function web_back_home(){
            goto('/home'+url_param, { replaceState: true }); // 浏览器替换当前历史记录
        }
        web_back_home();
    }catch (e){
        console.log("浏览器端不可用");
    }
    try {
        function server_back_home(){
            throw redirect(301, '/home'+url_param); // 服务器301永久重定向
        }
        server_back_home();
    }catch (e){
        console.log("服务端不可用");
    }


</script>