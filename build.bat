@echo off

setlocal

call "buildtemplates.bat"

pyinstaller ^
    --onefile ^
    --hidden-import glob ^
    --exclude-module arcpy ^
    --runtime-hook .\hooks\rthooks\pyi_rth_multiprocessing.py ^
    --runtime-hook .\hooks\rthooks\pyi_rth_arcpy.py ^
    --runtime-hook .\hooks\rthooks\pyi_rth_pyqt4.py ^
    --clean ^
    --noconsole ^
    -n ags_service_publisher_gui ^
    .\src\main.pyw

