<script lang="ts">
    import { resolve } from '$app/paths';
    import func from "../../common/func.svelte.js";
    import Example from "../../pages/_example/Example.svelte";

</script>

<svelte:head>
    <title>{func.get_translate("Example")}</title>
    <meta name="keywords" content="" />
    <meta name="description" content="" />
</svelte:head>

<section class="section-main scroll-y-style bg-neutral-100 dark:bg-neutral-900">
    <Example />
</section>