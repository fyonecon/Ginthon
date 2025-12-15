<script>
    import { resolve } from '$app/paths';
    import { page } from '$app/state';
    import func from "$lib/common/func.js";
    import Page404 from "$lib/pages/_404/_404.svelte";


</script>

<svelte:head>
    <title>{func.get_translate("_404")}</title>
    <meta name="keywords" content="" />
    <meta name="description" content="" />
</svelte:head>

<section class="section-main center scroll-y-style">
    <Page404 />
</section>