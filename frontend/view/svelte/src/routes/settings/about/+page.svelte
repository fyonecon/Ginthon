<script>
	import { resolve } from '$app/paths';
</script>

<svelte:head>
	<title>About</title>
    <meta name="keywords" content="" />
	<meta name="description" content="" />
</svelte:head>

<section class="section-main">
    <h1>About this app</h1>

    <p>
        <a href={resolve('/settings/about')}>About</a>
    </p>
</section>