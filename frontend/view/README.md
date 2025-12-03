# 本Svelte项目是Ginthon的默认视图使用的前端框架

Ginthon主项目：https://github.com/fyonecon/Ginthon

### 推荐IDE（webstorm）：
```
https://www.jetbrains.com/webstorm/download/?section=mac
```

===================================
# Svelte应用

### 常用命令：
在/frontend/view/目录运行：
```
npx sv create svelte
```

项目所在文件夹：/frontend/view/svelte/
```
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
		}),
		// 添加路径重写配置
        paths: {
            base: '', // 根据你的部署路径设置
            assets: '' // 根据你的部署路径设置。CDN如：'http://127.0.0.1:9100/view/svelte/dist'，，结尾无/
        },
	}
};

export default config;
```

在根index.html目录添加js调用py：
```
<script src="http://127.0.0.1:9100/js_must_data.js?cache="></script>
<script src="http://127.0.0.1:9100/js_call_py.js?cache="></script>
<script src="http://127.0.0.1:9100/js_func.js?cache="></script>
```

最终生成的静态网站目录：
```
/frontend/view/svelte/dist/
```

=================================

# vue项目

在/frontend/view/目录运行：
```
pnpm create vue@latest vue
```
项目所在文件夹：/frontend/view/vue/
```
pnpm install

pnpm run dev

pnpm run build
```
在根index.html目录添加js调用py：
```
<script src="http://127.0.0.1:9100/js_must_data.js?cache="></script>
<script src="http://127.0.0.1:9100/js_call_py.js?cache="></script>
<script src="http://127.0.0.1:9100/js_func.js?cache="></script>
```

最终生成的静态网站目录：
```
/frontend/view/vue/dist/
```

=================================

# 单页应用
将单页应用的首页index.html文件放置在：
```
/frontend/view/
```
单页应用的其它静态资源放置在：

（访问静态资源：http://127.0.0.1:9100/file/xxx ）
```
/frontend/file/
```

=================================
# 2025-12-03