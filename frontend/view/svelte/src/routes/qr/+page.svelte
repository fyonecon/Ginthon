<script lang="ts">
    import { resolve } from '$app/paths';
    import func from "../../common/func.svelte.js";
    import QR from "../../pages/qr/QR.svelte";

</script>

<svelte:head>
    <title>Make QR</title>
    <meta name="keywords" content="MakeQR,生成二维码" />
    <meta name="description" content="Make QR, 生成二维码。不收集任何隐私！" />
</svelte:head>

<section class="section-main scroll-y-style">
    <QR />
</section>