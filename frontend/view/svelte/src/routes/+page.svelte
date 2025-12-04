<script>
    import func from "$lib/common/func.js";

    // 重新定向 /到 /home 页面
    func.redirect_pathname({
        url_pathname: func.url_path("/home"),
        url_params: func.get_params(),
    });


</script>