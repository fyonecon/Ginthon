<script lang="ts">
    import { resolve } from '$app/paths';
    import { page } from '$app/state';
    import func from "$lib/common/func.svelte.js";

    //
    const route = func.get_route();
    // 或 let route = $state(func.get_route());
</script>

<div>
    <h3>{route}</h3>
</div>