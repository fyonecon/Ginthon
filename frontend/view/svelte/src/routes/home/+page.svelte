<script>
    import { resolve } from '$app/paths';
    import func from "$lib/common/func.svelte.js";
    import Home from "$lib/pages/home/Home.svelte";

</script>

<svelte:head>
    <title>{func.get_translate("Home")}</title>
    <meta name="keywords" content="" />
    <meta name="description" content="" />
</svelte:head>

<section class="section-main scroll-y-style  bg-white dark:bg-neutral-900">
    <Home />
</section>