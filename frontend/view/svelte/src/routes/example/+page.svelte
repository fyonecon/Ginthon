<script lang="ts">
    import { resolve } from '$app/paths';
    import func from "$lib/common/func.svelte.js";
    import Example from "$lib/pages/example/Example.svelte";

</script>

<svelte:head>
    <title>Example</title>
    <meta name="keywords" content="" />
    <meta name="description" content="" />
</svelte:head>

<section class="section-main scroll-y-style bg-white dark:bg-neutral-900">
    <Example />
</section>