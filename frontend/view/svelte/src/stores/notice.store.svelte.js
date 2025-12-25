
import { createToaster } from '@skeletonlabs/skeleton-svelte';

const toaster = createToaster({
    placement: 'top-end',
});

export const notice_data = $state({
    toaster: toaster,
});