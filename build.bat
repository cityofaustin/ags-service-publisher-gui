@echo off

setlocal

call "%~dp0buildtemplates.bat"

pyinstaller ^
    --onefile ^
    --hidden-import glob ^
    --hidden-import imp ^
    --hidden-import uuid ^
    --exclude-module arcpy ^
    --exclude-module numpy ^
    --upx-exclude msvcp140.dll ^
    --upx-exclude msvcp140_1.dll ^
    --upx-exclude msvcp140_2.dll ^
    --upx-exclude python36.dll ^
    --upx-exclude qwindows.dll ^
    --upx-exclude qwindowsvistastyle.dll ^
    --upx-exclude ucrtbase.dll ^
    --upx-exclude vcruntime140.dll ^
    --upx-exclude vcruntime140_1.dll ^
    --additional-hooks-dir=%~dp0hooks ^
    --runtime-hook %~dp0hooks\rthooks\pyi_rth_arcpy.py ^
    --add-binary %~dp0\..\ags-service-publisher\resources\arcgis\projects\blank\blank.aprx;resources/arcgis/projects/blank ^
    --clean ^
    --noconsole ^
    --distpath %~dp0dist ^
    --workpath %~dp0build ^
    --specpath %~dp0 ^
    -n ags_service_publisher_gui ^
    %~dp0src\main.pyw
