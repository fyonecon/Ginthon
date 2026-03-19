<script lang="ts">
    import { resolve } from '$app/paths';
    import func from "../../common/func.svelte.js";
    import Info from "../../pages/info/Info.svelte";

</script>

<svelte:head>
    <title>{func.get_translate("Info")}</title>
    <meta name="keywords" content="" />
    <meta name="description" content="" />
</svelte:head>

<section class="section-main scroll-y-style">
    <Info />
</section>