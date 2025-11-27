# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# 直接定义 frontend 文件，不需要复杂函数
datas = []

# 手动添加 frontend 文件夹
frontend_files = [
    ('frontend/favicon.ico', 'frontend'),
    ('frontend/launcher.png', 'frontend'),
    ('frontend/view/index.html', 'frontend/view'),
    # 添加 tray 文件夹中的 7z 文件
    ('frontend/tray/', 'frontend/tray'),
    #('frontend/tray/mac.7z', 'frontend/tray'),
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
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='frontend/favicon.ico',
)