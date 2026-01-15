<script lang="ts">
    import { resolve } from '$app/paths';
    import { page } from '$app/state';
    import func from "../../common/func.svelte.js";
    import Page404 from "../../pages/_404/_404.svelte";


</script>

<svelte:head>
    <title>{func.get_translate("_404")}</title>
    <meta name="keywords" content="" />
    <meta name="description" content="" />
</svelte:head>

<section class="section-main center scroll-y-style bg-neutral-100 dark:bg-neutral-900">
    <Page404 />
</section>