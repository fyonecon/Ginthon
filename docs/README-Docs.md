### 【手动】开发环境逐步运行项目：
1. 开发环境运行视图UI：
> cd ./frontend/view/svelte
> 
> npx sv add tailwindcss
> 
> npm run dev

2. 开发环境直接运行状态栏托盘：
> python gthon_tray.py

3. 开发环境运行软件（加载 localhost npm 动态文件）：
> python gthon_window.py --cmd dev

4. 开发环境运行软件（加载 127.0.0.1 dist 静态文件）：
> python gthon_window.py --cmd build

(注意，直接运行“python window.py” == “python window.py --cmd build”，window.py加载的是svelte的dist静态文件，使用127.0.0.1域名。而“python window.py --cmd dev”加载的是svelte的“pnpm run dev”本地localhost网页。)

### 【手动】打包程序为程序安装包：
1. 生成视图UI dist静态文件：
> cd ./frontend/view/svelte
> 
> npm run build

2. 打包成桌面安装包：
> pyinstaller --clean gthon_window.spec
> 

### 其它：打包成安装程序（win、mac、linux）：
（如有需要请手动删除/dist/ 和 /build/ 文件夹）
（只能打包当前平台CPU结构的程序。也可以使用“python build.py”命令一键打包）
> 
> pyinstaller --clean gthon_window.spec 
>

### 视图UI配置教程（Svelte、VUE）：
🔥请查看本目录文件/frontend/view/README.md

### 状态栏托盘Tray运行原理：
原理：由于视图主程序已经是主线程，mac中不能存在第二主线程（NSWindow影响）。所以本程序在视图主程序中以多线程的方式，利用shell拉起打包成二进制的Tray程序。

在开发的过程中，运行dev.py或build.py都会自动执行打包程序，无需担心window主程序没有挂载“tray_create()”。

dev过程：打包Tray二进制文件--将二进制文件移动到frontend/tray文件夹--启动pnpm--启动window--shell启动二进制文件。

build过程：打包Tray二进制文件--将二进制文件移动到frontend/tray文件夹--pnpm打包视图UI--打包frontend+PY文件。

### 常用pip安装库：
如果遇到网络忙或者下载错误，多试几次，不需要更换镜像源（使用官方源即可）。
#### 爬虫
```
pip3 install requests

pip3 install beautifulsoup4

pip3 install lxml

pip3 install fake-useragent
 
pip3 install asyncio

pip3 install httpx
 
pip3 install selenium
 
pip3 install scrapy

pip3 install Playwright

pip3 install pyinstaller

pip3 install py7zr

```

#### 服务或框架
```
pip3 install flask

pip3 install pywebview

pip3 install schedule

pip3 install pystray

pip3 install pycryptodome

```

#### 读写office文件
```
pip3 install xlrd
 
pip3 install xlwt
 
pip3 install xlutils

pip3 install xlwings
 
pip3 install XlsxWriter
 
pip3 install openpyxl
 
pip3 install pandas
```