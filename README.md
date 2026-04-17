
## Ginthon是用Python+Web写的“视图窗口+稳定服务”的桌面端（Win、Mac、Linux）多功能程序基座。项目结构清晰，功能划分合理，适合大项目，开箱即用但是有一定上手门槛。
```
代码习惯无复杂继承和类。

ApacheV2 License。

Ginthon 基于 pywebview、flask 等。无 PyQT。ApacheV2 License。

GUI 前端默认 Svelte5，运行于 Webview2、Webkit、WebKitGTK 中。

打包安装包体积在 55MB 左右，RAM 占用 170MB 左右。

全静态，可挂载其它语言程序编写的二进制子程序。

代码目前只在Git^hu^b上发布（防^爬说明20251116）。

开源地址：https://github.com/fyonecon/Ginthon 。
```

### 老一辈艺术家提醒：

Python版基座请戳：https://github.com/fyonecon/Ginthon 。

Golang版基座请戳：https://github.com/fyonecon/Waigo 。

Go和Py都是以“尽量‘返回默认值’代替‘抛出Error’”+“尽量复用函数”+“尽量不使用继承”+“减少不必要的外部import”为原则。

---

### 程序要求：
```
需要 Python3.14+

需要 ES2023+ 基础环境

已适配macOS14+、Win10+。Linux2024+(Linux环境尚未验证)。完整支持2024年年初更新或发布的电脑系统。

开发IDE PyCharm（推荐）

```

### 拉取仓库：
窗口及服务·主程序（Ginthon-Main）：
> git clone -b main https://github.com/fyonecon/Ginthon.git Ginthon-Main

### 初始化项目：
1. 安装 .venv 虚拟环境：
```
以PyCharm为例：

（删除老 .venv ，有就删除）-- 设置 -- Python -- Interpreter -- Add Interpreter -- Add local interpreter -- 选择 Generate New --- 选择 Virtualenv -- 创建新的.venv即可。
```

2. 初始化项目 Py 依赖：
> pip install -r requirements.txt

3. 导出或更新项目所有依赖：
> pip freeze > requirements.txt

4. 清除不必要的项目依赖：
```
删除.venv文件夹，重新初始化项目依赖即可.
```
5. 安装npm依赖及项目 node_modules：
> cd ./frontend/view/svelte
> 
> npx sv add tailwindcss
> 
> npm install
>

---

### 开发环境运行项目：
> #在dev环境默认展开console，build环境默认无console。
> 
> python dev.py

### 打包成桌面安装包（.app、.exe、.deb等）：
> #底层使用 pyinstaller 打包。仅打包当前"CPU类型+操作系统类型"的安装包。
> 
> python build.py

---

### 项目结构：

#### Py命名原则：
+ 系统集文件夹名或文件名：小写+下划线
+ 自定义文件夹名：小驼峰
+ 自定义函数：小驼峰
+ 自定义变量：小驼峰
+ 自定义接口名：小写+下划线

#### Frontend命名原则：
+ 函数及变量：小写+下划线
+ 引号：双引号 使用优先于 单引号

```text
Ginthon-Main
├── build 打包运行时目录（自动生成）
├── dist 程序打包文件目录（自动生成。这里存放你打包后的app安装包）
├── frontend 前端或静态文件
│   ├── file 放其他web文件，额外的web文件
│   ├── tray （状态托盘二进制文件，自动创建）
│   └── view 前端视图（可多视图框架切换）
│       └── svelte 视图UI（默认SvelteKit）
│           ├── src 视图发开发文件
│           │   └── common 公共函数
│           │   └── pages 页面具体实现
│           │   └── parts 公用Svelte组件
│           │   └── stores 绑定数据管理
│           │   └── services 内置服务
│           │   └── routes 路由、layout、公共参数验证
│           ├── config.js 配置文件
│           └── static 静态文件
│       ├── vue 视图UI（查看文件/frontend/view/README.md）
│       ├── index.html （单页应用请使用此文件）
│       ├── readme.md 🔥前端操作记录与教程
├── internal 后段时间或py核心代码
│   ├── app 自定义的App功能
│   │   ├── flask Web控制器目录
│   │   ├── tray 状态栏托盘
│   │   └── window 窗口服务目录
│   │       ├── controller
│   │       │   ├── do_events.py 操作窗口事件
│   │       │   ├── js_call_py.py js调用py对照表
│   │       │   ├── on_events.py 窗口运行事件
│   │       │   ├── py_run_js.py py调用js对照表
│   │       │   └── tray_events.py
│   │       ├── window_route.py 窗口必要页面相关路由
│   │       └── window_view.py 窗口页面html代码
│   ├── bootstrap 框架加载核心
│   │   ├── app_auth.py 认证与密钥相关
│   │   ├── init_sys.py 检查系统及硬件
│   │   ├── init_window.py 窗口服务
│   │   ├── run_check_sys.py
│   │   ├── run_flask.py Web服务
│   │   ├── run_tray.py 启动状态栏托盘
│   │   └── run_services.py 其它主页服务
│   ├── common 公共函数、封装的kit
│   │   ├── kits 公共函数的Kit
│   │   │   ├── _7z.py 7Z解压
│   │   │   ├── FILETYPE_DICT.py 各种文件对照表
│   │   │   ├── ICON.py 程序icon的二进制
│   │   │   ├── main_dirpath.py 虚拟路径
│   │   │   ├── secret_aes.py 对称加密
│   │   │   ├── shell.py PY运行shell
│   │   │   ├── time_interval.py 定时器
│   │   │   ├── txt_data.py 简单的文件型数据库
│   │   │   ├── watch_pid.py
│   │   │   └── watch_processes.py
│   │   ├── func.py 公共函数
│   │   ├── request_data.go 公用处理Flask Input请求参数函数
│   │   └── translate.py 多语言翻译对照表
│   └── config.py 系统配置信息
│   ├── routes 自定义的路由
│   │   └── ...py 
│   ├── services 服务
│   │   ├── flask_middleware.py Web检测中间件
│   │   └── services_for_time_interval.py 定时器
├── LICENSE
├── README.md 项目说明
├── README-Docs.md 项目原理说明
├── requirements-win.txt Win下的依赖
├── requirements.txt 默认依赖
├── build.json 打包程序的配置文件
├── build.py 打包程序一键运行
├── dev.json 开发环境运行的配置文件
├── dev.py 开发环境一键运行
├── gthon_tray.py 状态栏托盘入口
├── gthon_tray.spec PYinstaller的SPEC打包文件参数
├── gthon_window.py 视窗主程序入口
└── gthon_window.spec PYinstaller的SPEC打包文件参数
```

### 运行效果：
![运行效果](./docs/show.png)

---

### Python教程：

> Python3：https://www.runoob.com/python3/python-queue.html
>
> Flask：https://flask.palletsprojects.com/en/stable/installation/#install-flask
>
> PyWebview：https://pywebview.idepy.com/guide/usage.html
>
> Skeleton UI：https://www.skeleton.dev/docs/svelte/guides/mode
> 
> Tailwind CSS：https://www.tailwindcss.cn/docs/installation
> 
> Iconify SVG：https://icon-sets.iconify.design/

### Mac安装Homebrew国内源
#### 苹果电脑安装脚本（选择清华大学镜像）：
> /bin/zsh -c "$(curl -fsSL https://gitee.com/cunkai/HomebrewCN/raw/master/Homebrew.sh)"

#### 苹果电脑卸载脚本：
> /bin/zsh -c "$(curl -fsSL https://gitee.com/cunkai/HomebrewCN/raw/master/HomebrewUninstall.sh)"

### 安装Python

安装Python：
参考：https://geek-blogs.com/blog/how-to-uninstall-and-reinstall-python-mac/

方法1；使用官方安装包安装（不推荐）：
下载安装包：https://www.python.org/downloads/

方法2: 使用brew（推荐）:

> brew install python@3.14

查看安装的版本：
> python3 --version
> pip3 --version

### 卸载Python

1. 官方安装包安装的： 

找到 Python 安装目录：
> sudo rm -rf /Library/Frameworks/Python.framework/Versions/3.x

注意：3.x 是你要卸载的 Python 版本号，如 3.9 等
删除相关的应用程序：
> sudo rm -rf /Applications/Python\ 3.x

2. brew方法安装的：

> brew uninstall python@3.14

### 开发工具IDE：pycharm-community：
不推荐使用vscode。
> https://www.jetbrains.com.cn/edu-products/download/download-thanks-pce.html
> 
>（https://download.jetbrains.com/python/pycharm-community-2025.2.4.exe ）
> 
>（https://download.jetbrains.com/python/pycharm-community-2025.2.4.dmg ）
> 
>（https://download.jetbrains.com/python/pycharm-community-2025.2.4-aarch64.dmg ）

---

其它原理请戳 ./docs/README-Docs.md 文档。

---

# start 2025-11-15