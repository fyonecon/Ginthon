<script lang="ts">
    import { resolve } from '$app/paths';
    import func from "../../common/func.svelte.js";
    import PlayAudio from "../../pages/play_audio/PlayAudio.svelte";

</script>

<svelte:head>
    <title>{func.get_translate("PlayAudio")}</title>
    <meta name="keywords" content="" />
    <meta name="description" content="" />
</svelte:head>

<section class="section-main scroll-y-style ">
    <PlayAudio />
</section>