# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# 直接定义 frontend 文件，不需要复杂函数
datas = []

# 手动添加 frontend 文件夹
frontend_files = [
    # 单独添加文件
    ('frontend/favicon.ico', 'frontend'),
    ('frontend/icon.png', 'frontend'),
    ('frontend/view/index.html', 'frontend/view'),
    # 添加 /tray/ 和 /view/ 文件夹中的全部文件
    ('frontend/tray/', 'frontend/tray'), # 状态拉托盘
    #('frontend/view/', 'frontend/view'), # 单页应用
    #('frontend/view/vue/dist/', 'frontend/view/vue/dist'), # VUE
    ('frontend/view/svelte/dist/', 'frontend/view/svelte/dist'), # Svelte
    # 添加整个文件夹
    #('frontend/file/', 'frontend/file'),
]

datas.extend(frontend_files)

a = Analysis(
    ['window.py'],
    pathex=[],  # 可以为空，PyInstaller 会自动处理
    binaries=[],
    datas=datas,
    hiddenimports=[
        'flask',
        'pywebview',
        'webview',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# Win
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Ginthon', # 文件名或应用名
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True, # UPX。False
    upx_exclude=[],
    runtime_tmpdir=None,
    argv_emulation=True,  # 对GUI应用重要。True
    target_arch=None,
    #codesign_identity=None,
    #entitlements_file=None,
    icon='./frontend/icon.ico', # win必须.ico，此处适配win、Linux
    console=False,
    disable_windowed_traceback=False,
)

# Mac：创建 .app bundle
app = BUNDLE(
    exe,
    name='Ginthon.app',  # .app 的名称
    icon='./frontend/icons.icns', # mac必须.icns
    bundle_identifier='top.datathink.ginthon',  # 可选：bundle identifier
#    entitlements_file='./frontend/entitlements.plist',  # 提前申请一些权限
    info_plist={
        'CFBundlePackageType': 'APPL',
        'CFBundleName': 'Ginthon',
        'CFBundleDisplayName': 'Ginthon',
        'CFBundleIdentifier': 'top.datathink.ginthon',
        'CFBundleShortVersionString': '1.4.0',      # 显示版本
        'CFBundleVersion': '1.4.x',                     # 构建版本(日期、版本号、其它数字)
        'CFBundleDevelopmentRegion': 'zh-CN',       # 开发地区
        'NSHumanReadableCopyright': '© Datathink.Top',
        'LSMinimumSystemVersion': '12.0',        # 最低系统要求
        'NSHighResolutionCapable': 'True',          # 支持 Retina
        'LSUIElement': True,                       # 是否显示Dock图标。 True
#        'NSSupportsAutomaticTermination': False,
#        'NSQuitAlwaysKeepsWindows': True,
##        'LSBackgroundOnly': False,
#        'NSPrincipalClass': 'NSApplication',
#        'LSEnvironment': {
#            'PYWEBVIEW_GUI': 'webkit',  # 强制使用 WebKit
#        },
        ###
        # 无签名时请启用如下，否则Mac系统会延迟15s打开程序窗口：
        # 关键配置：禁用 Gatekeeper 延迟
        'LSFileQuarantineEnabled': False,
        'LSEnvironment': {
            'PYTHONOPTIMIZE': '2',
        },
        # 禁用沙盒
        #'com.apple.security.app-sandbox': False,
        # 告诉系统这是一个本地应用，不需要验证
        #'NSUIPersistentDownloadsDirectory': '~/Downloads',
        ###
    },
)
