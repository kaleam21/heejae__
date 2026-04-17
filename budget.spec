# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('app.html', '.')],
    hiddenimports=['webview', 'webview.platforms.winforms', 'webview.platforms.cocoa', 'webview.platforms.gtk'],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='가계부',
    debug=False,
    strip=False,
    upx=True,
    console=False,
    icon=None,
)

app = BUNDLE(
    exe,
    name='가계부.app',
    icon=None,
    bundle_identifier='com.budget.app',
)
