<script lang="ts">

import func from "$lib/common/func.svelte.js";
import config from "$lib/config.js";
</script>

<section class="section-foot select-none  pywebview-drag-region can-drag bg-white dark:bg-neutral-900">
    <div class="center" style="opacity: 0.2; line-height: 40px;">
        {config.app.app_name}
    </div>
</section>

<style>
    .section-foot {
        position: fixed;
        z-index: 0;
        width: calc(100% - 220px);
        height: 40px;
        bottom: 0;
        right: 0;
        overflow-x: hidden;
        overflow-y: hidden;
    }
</style>