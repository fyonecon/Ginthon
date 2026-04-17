<script lang="ts">
    import { resolve } from '$app/paths';
    import func from "../../common/func.svelte.js";
    import ITHome from "../../pages/it_home/ITHome.svelte";

</script>

<svelte:head>
    <title>{func.get_translate("ITHome")}</title>
    <meta name="keywords" content="" />
    <meta name="description" content="" />
    <link rel="icon" type="image/png" href="./launcher.png" />
</svelte:head>

<section class="section-main scroll-y-style bg-neutral-100 dark:bg-neutral-900">
    <ITHome />
</section>