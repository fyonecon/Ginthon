<script>
    import func from "$lib/common/func.js";
    import config from "$lib/config.js";

    // 重新定向 /到 /home 页面
    func.redirect_pathname({
        url_pathname: func.url_path(config.sys.home_route),
        url_params: func.get_params(),
    });


</script>