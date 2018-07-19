@echo off

setlocal

call "%~dp0buildtemplates.bat"

pyinstaller ^
    --onefile ^
    --hidden-import glob ^
    --hidden-import uuid ^
    --exclude-module arcpy ^
    --exclude-module numpy ^
    --runtime-hook .\hooks\rthooks\pyi_rth_arcpy.py ^
    --clean ^
    --noconsole ^
    -n ags_service_publisher_gui ^
    %~dp0src\main.pyw
