# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# 直接定义 frontend 文件，不需要复杂函数
datas = []

# 手动添加 frontend 文件夹
frontend_files = [
    ('frontend/favicon.ico', 'frontend'),
    ('frontend/launcher.png', 'frontend'),
]

datas.extend(frontend_files)

a = Analysis(
    ['tray.py'],
    pathex=[],  # 可以为空，PyInstaller 会自动处理
    binaries=[],
    datas=datas,
    hiddenimports=[
        'pystray',
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
    name='tray', # 文件名或应用名
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