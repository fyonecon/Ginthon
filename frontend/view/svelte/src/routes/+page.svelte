<script lang="ts">
    /*根路由*/
    import { resolve } from '$app/paths';
    import func from "../common/func.svelte.js";
    import Index from "../pages/index/Index.svelte";
</script>

<svelte:head>
    <title></title>
    <meta name="keywords" content="" />
    <meta name="description" content="" />
    <link rel="icon" type="image/png" href="./launcher.png" />
</svelte:head>

<section class="section-main scroll-y-style">
    <Index />
</section>