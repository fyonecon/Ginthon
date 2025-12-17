<script>
    import { resolve } from '$app/paths';
    import func from "$lib/common/func.svelte.js";
    import Settings from "$lib/pages/settings/Settings.svelte";
</script>

<svelte:head>
    <title>{func.get_translate("Settings")}</title>
    <meta name="keywords" content="" />
    <meta name="description" content="" />
</svelte:head>

<section class="section-main scroll-y-style bg-white dark:bg-black">
    <Settings />
</section>