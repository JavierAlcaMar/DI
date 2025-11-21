# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['MiniOffice.py'],
    pathex=[],
    binaries=[],
    datas=[('imagesMO', 'imagesMO')],
    hiddenimports=[],
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
    [],
    exclude_binaries=True,
    name='MiniOffice',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['imagesMO/iconoApp.icns'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='MiniOffice',
)
app = BUNDLE(
    coll,
    name='MiniOffice.app',
    icon='imagesMO/iconoApp.icns',
    bundle_identifier=None,
)
