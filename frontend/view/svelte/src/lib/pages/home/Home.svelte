<script>
    import { resolve } from '$app/paths';
    import { page } from '$app/state';
    import func from "$lib/common/func.js";

    //
    const route = func.get_route();
</script>

<div>
    <h3>{route}</h3>
    <p>{window.location.href}</p>
    <p>{window.navigator.userAgent}</p>
</div>