//import adapter from '@sveltejs/adapter-auto';
import adapter from '@sveltejs/adapter-static';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	kit: {
		// adapter-auto only supports some environments, see https://svelte.dev/docs/kit/adapter-auto for a list.
		// If your environment is not supported, or you settled on a specific environment, switch out the adapter.
		// See https://svelte.dev/docs/kit/adapters for more information about adapters.
		adapter: adapter({
			// default options are shown. On some platforms
			// these options are set automatically — see below
			pages: './dist',
			assets: './dist',
			fallback: '404.html',
			precompress: false,
			strict: true
		}),
        // 添加路径重写配置
        paths: {
            base: '/view', // 根据你的部署路径设置，''、'/view'、'/view_static'，此值请同样 config.js--sys--base_route 里面设置
            assets: '', // 根据你的部署路径设置。CDN如：'http(s)://127.0.0.1:9750/view/svelte/dist'，结尾无/
        },
	}
};

export default config;
