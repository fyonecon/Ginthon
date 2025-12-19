# Ginthon视图使用的前端框架（搭建与设置）

Ginthon主项目：https://github.com/fyonecon/Ginthon

### 推荐IDE（webstorm）：
```
https://www.jetbrains.com/webstorm/download/?section=mac
```

===================================
# Svelte应用（默认）

### 常用命令：
在/frontend/view/目录运行：
```
npx sv create svelte
```

更改端口为9770（本地开发环境用）:
```
在vite.config.js中设置：

server: {
    port: 9770, // 固定端口为 9770
    strictPort: true, // 如果端口被占用，不自动选择其他端口
    host: true // 允许外部访问（可选）
}
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
在/frontend/view/svelte/svelte.config.js添加如下内容:
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
            assets: '' // 根据你的部署路径设置。CDN如：'http://127.0.0.1:9750/view/svelte/dist'，，结尾无/
        },
	}
};

export default config;
```

将如下js添加至/svelte/src/app.html的头部head之中：
```
<script src="http://127.0.0.1:9750/js_must_data.js?cache=v1.4.0"></script>
```

最终生成的静态网站目录：
```
/frontend/view/svelte/dist/
```

在Ginthon/internal/config.py中设置静态文件参数：
```
"pywebview": { # window
    "view_url": "http://127.0.0.1:port", # 视图网址（协议+网址+端口+路径，如：http://127.0.0.1 ）
    "view_class": "svelte", # 视图使用的模板（影响flask服务器加载页面）。 "vue"、"svelte"、单页填""
    "view_file_html": "view/svelte/dist", # pnpm run build后的dist目录。 "view/vue/dist"、"view/svelte/dist"、单页应用""。结尾无/。
},
```

=================================

# vue项目

在/frontend/view/目录运行：
```
pnpm create vue@latest vue
```

更改端口为9770（本地开发环境用）:
```
在vite.config.js中设置：

server: {
    port: 9770, // 固定端口为 9770
    strictPort: true, // 如果端口被占用，不自动选择其他端口
    host: true // 允许外部访问（可选）
}
```

项目所在文件夹：/frontend/view/vue/
```
pnpm install

pnpm run dev

pnpm run build
```

将如下js添加至/vue/src/index.html的头部head之中：
```
<script src="http://127.0.0.1:9750/js_must_data.js?cache=v1.4.0"></script>
```

最终生成的静态网站目录：
```
/frontend/view/vue/dist/
```

在Ginthon/internal/config.py中设置静态文件参数：
```
"pywebview": { # window
    "view_url": "http://127.0.0.1:port", # 视图网址（协议+网址+端口+路径，如：http://127.0.0.1 ）
    "view_class": "vue", # 视图使用的模板（影响flask服务器加载页面）。 "vue"、"svelte"、单页填""
    "view_file_html": "view/vue/dist", # pnpm run build后的dist目录。 "view/vue/dist"、"view/svelte/dist"、单页应用""。结尾无/。
},
```

=================================

# 单页应用
将单页应用的首页index.html文件放置在：
```
/frontend/view/
```
单页应用的其它静态资源放置在：

（访问静态资源：http://127.0.0.1:9750/file/xxx ）
```
/frontend/file/
```

=================================
# 2025-12-03