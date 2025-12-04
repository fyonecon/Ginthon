<script>
    import { resolve } from '$app/paths';
    import func from "$lib/common/func.js";
    import Settings from "$lib/pages/settings/Settings.svelte";
</script>

<svelte:head>
    <title>Settings</title>
    <meta name="keywords" content="" />
    <meta name="description" content="" />
</svelte:head>

<section class="section-main scroll-y-style">
    <Settings />
</section>