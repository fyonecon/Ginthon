// 全局页面
export const prerender = true;
export const csr = true; // 确保客户端渲染
export const ssr = false // false 关闭SEO，true 页面编译成SEO。（false可以让js正确访问“window”对象）