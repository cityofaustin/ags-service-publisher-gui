@echo off

setlocal

call "%~dp0buildtemplates.bat"

pyinstaller ^
    --onefile ^
    --hidden-import glob ^
    --hidden-import uuid ^
    --exclude-module arcpy ^
    --exclude-module numpy ^
    --runtime-hook %~dp0hooks\rthooks\pyi_rth_arcpy.py ^
    --runtime-hook %~dp0hooks\rthooks\pyi_rth_pyqt4.py ^
    --clean ^
    --noconsole ^
    --distpath %~dp0dist ^
    --workpath %~dp0build ^
    --specpath %~dp0 ^
    -n ags_service_publisher_gui ^
    %~dp0src\main.pyw
