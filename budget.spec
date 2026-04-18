# -*- mode: python ; coding: utf-8 -*-

import sys

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('app.html', '.')],
    hiddenimports=[
        'webview',
        'webview.platforms.winforms',
        'webview.platforms.cocoa',
        'webview.platforms.gtk',
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
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
    name='가계부',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    icon=None,
)

app = BUNDLE(
    exe,
    name='가계부.app',
    icon=None,
    bundle_identifier='com.kaleam21.budget',
    info_plist={
        'NSHighResolutionCapable': True,
        'CFBundleShortVersionString': '1.1.0',
    },
)
