<script>
    import { resolve } from '$app/paths';
    import { page } from '$app/state';
    import func from "$lib/common/func.js";

    // 链接携带的信息
    const error_url = func.search_param("error_url")
    const error_msg = func.search_param("error_msg");
    const back_url = func.url_path('/home')+'?from=404';

</script>

<svelte:head>
    <title>404</title>
    <meta name="keywords" content="" />
    <meta name="description" content="" />
</svelte:head>

<section class="section-main center scroll-y-style">
    <div>
        <h2>{error_msg?error_msg:"404"}</h2>
        <p>{error_url}</p>
        <p>
            <a href={resolve(back_url)}>⬅️ 返回首页</a>
        </p>
    </div>
</section>