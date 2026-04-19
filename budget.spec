# -*- mode: python ; coding: utf-8 -*-
import sys
import os

block_cipher = None

# macOS SSL 인증서 (certifi) 포함
datas = []
try:
    import certifi
    datas.append((certifi.where(), 'certifi'))
except ImportError:
    pass

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[
        'webview',
        'webview.platforms.winforms',
        'webview.platforms.cocoa',
        'webview.platforms.gtk',
        'certifi',
        'ssl',
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
    name='budget',
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
