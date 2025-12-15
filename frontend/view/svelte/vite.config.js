import tailwindcss from '@tailwindcss/vite';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [tailwindcss(), sveltekit()],

	server: {
		port: 9770, // 固定端口为 9770
		strictPort: true, // 如果端口被占用，不自动选择其他端口
		host: false // 允许外部访问（可选）
	}
});
