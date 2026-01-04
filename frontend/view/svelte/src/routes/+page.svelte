<script lang="ts">
    import func from "../common/func.svelte.js";
    import config from "../config.js";

    // 重新定向 /到 /home 页面
    func.redirect_pathname({
        url_pathname: func.url_path(config.sys.base_route+config.sys.home_route),
        url_params: func.get_params(),
    });


</script>