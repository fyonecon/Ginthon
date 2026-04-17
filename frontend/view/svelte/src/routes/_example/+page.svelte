<script lang="ts">
    import { resolve } from '$app/paths';
    import func from "../../common/func.svelte.js";
    import Example from "../../pages/_example/Example.svelte";

</script>

<svelte:head>
    <title>{func.get_translate("Example")}</title>
    <meta name="keywords" content="" />
    <meta name="description" content="" />
    <link rel="icon" type="image/png" href="./launcher.png" />
</svelte:head>

<section class="section-main scroll-y-style">
<!--<section class="section-main scroll-y-style bg-white dark:bg-surface-950">-->
<!--<section class="section-main scroll-y-style bg-neutral-100 dark:bg-neutral-900">-->
<!--<section class="section-main scroll-y-style bg-white dark:bg-black">-->
    <Example />
</section>