# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

datas = [('templates', 'templates'), ('src/styles.qss', 'src')]
binaries = [('libs/libgobject-2.0-0.dll', '.'), ('libs/libglib-2.0-0.dll', '.'), ('libs/libpango-1.0-0.dll', '.'), ('libs/libcairo-2.dll', '.'), ('libs/libharfbuzz-0.dll', '.'), ('libs/libfontconfig-1.dll', '.'), ('libs/libpangoft2-1.0-0.dll', '.')]
hiddenimports = ['jinja2', 'weasyprint', 'sqlite3']
tmp_ret = collect_all('PyQt6')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


a = Analysis(
    ['src\\main.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='NeuroMedic',
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
    icon=['iconoNM.ico'],
)
