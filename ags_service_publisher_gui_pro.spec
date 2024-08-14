# -*- mode: python ; coding: utf-8 -*-
import fnmatch
import os
from PyInstaller.utils.hooks import collect_data_files, get_package_paths

datas = []
datas += collect_data_files('archook')

a = Analysis(
    ['src\\main.pyw'],
    pathex=[],
    binaries=[(os.path.join(get_package_paths('ags_service_publisher')[1], r'resources\arcgis\projects\blank\blank.aprx'), 'ags_service_publisher/resources/arcgis/projects/blank')],
    datas=datas,
    hiddenimports=[
        'archook',
        'glob',
        'imp',
        'uuid'
    ],
    hooksconfig={},
    runtime_hooks=['hooks/rthooks/pyi_rth_arcpy.py'],
    excludes=['arcpy', 'numpy'],
    noarchive=False,
    optimize=0,
)

# Exclude unused Qt dependencies, translations, and plugins.
to_keep = []
to_exclude = {
    '*.qm',
    'd3dcompiler_*.dll',
    'libGLESv*.dll',
    'opengl32sw.dll',
    'qgif.dll',
    'qicns.dll',
    'qico.dll',
    'qjpeg.dll',
    'qminimal.dll',
    'qoffscreen.dll',
    'qpdf.dll',
    'qsvg.dll',
    'qsvgicon.dll',
    'Qt6Network.dll',
    'Qt6Pdf.dll',
    'Qt6Svg.dll',
    'qtga.dll',
    'qtiff.dll',
    'qtuiotouchplugin.dll',
    'qwbmp.dll',
    'qwebgl.dll',
    'qwebp.dll',
    'qxdgdesktopportal.dll',
}

# Iterate through the list of included binaries.
for (dest, source, kind) in a.binaries:
    # Skip anything we don't need.
    if any(fnmatch.fnmatch(os.path.basename(dest), exclusion) for exclusion in to_exclude):
        continue
    to_keep.append((dest, source, kind))

# Replace list of data files with filtered one.
a.binaries = to_keep

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='ags_service_publisher_gui_pro',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
