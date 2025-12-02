### 本Svelte项目是Ginthon的默认视图使用的前端框架

Ginthon主项目：https://github.com/fyonecon/Ginthon

### 推荐IDE（webstorm）：
```
https://www.jetbrains.com/webstorm/download/?section=mac
```
### 常用命令：
项目所在文件夹：/frontend/view/svelte/
```
npx sv create svelte

pnpm install

pnpm run dev

pnpm run build
```

### Svelte打包静态网站：
静态网站请参考：
https://svelte.dev/docs/kit/adapters
```
pnpm i -D @sveltejs/adapter-static
```
在svelte.config.js添加如下内容:
```
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
			pages: 'dist',
			assets: 'dist',
			fallback: '404.html',
			precompress: false,
			strict: true
		})
	}
};

export default config;
```
最终生成的静态网站目录：
```
/frontend/view/svelte/dist/
```

### 2025-12-03