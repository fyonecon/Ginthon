<script lang="ts">
    import { resolve } from '$app/paths';
    import func from "../../common/func.svelte.js";
    import Settings from "../../pages/settings/Settings.svelte";
</script>

<svelte:head>
    <title>{func.get_translate("Settings")}</title>
    <meta name="keywords" content="" />
    <meta name="description" content="" />
</svelte:head>

<section class="section-main scroll-y-style bg-neutral-100 dark:bg-neutral-900">
    <Settings />
</section>