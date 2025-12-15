import { writable } from 'svelte/store';

export const sideTabData = writable({
    tab_value: "",
    tab_name: "",
});