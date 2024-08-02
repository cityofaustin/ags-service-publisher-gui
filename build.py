import PyInstaller.__main__

PyInstaller.__main__.run([
    'ags_service_publisher_gui_pro.spec',
    '--distpath', 'dist',
    '--workpath', 'build',
    '--clean',
    '--noconfirm',
])
