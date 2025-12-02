<script>
	import { resolve } from '$app/paths';
</script>

<svelte:head>
	<title>About</title>
    <meta name="keywords" content="" />
	<meta name="description" content="About" />
</svelte:head>

<div class="text-column">
	<h1>About this app</h1>

	<p>
		The <a href={resolve('/sverdle')}>Sverdle</a> page illustrates SvelteKit's data loading and form
		handling. Try using it with JavaScript disabled!
	</p>
</div>
