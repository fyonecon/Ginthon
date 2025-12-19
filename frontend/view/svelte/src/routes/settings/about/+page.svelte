<script lang="ts">
	import { resolve } from '$app/paths';
    import func from "../../../common/func.svelte.js";
    import About from "../../../pages/settings/about/About.svelte";
</script>

<svelte:head>
	<title>{func.get_translate("About")}</title>
    <meta name="keywords" content="" />
	<meta name="description" content="" />
</svelte:head>

<section class="section-main scroll-y-style bg-white dark:bg-neutral-900">
    <About/>
</section>