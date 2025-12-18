<script lang="ts">
    import { resolve } from '$app/paths';
    import func from "$lib/common/func.svelte.js";
    import ITHome from "$lib/pages/ithome/ITHome.svelte";

</script>

<svelte:head>
    <title>ITHome</title>
    <meta name="keywords" content="" />
    <meta name="description" content="" />
</svelte:head>

<section class="section-main scroll-y-style bg-white dark:bg-neutral-900">
    <ITHome />
</section>