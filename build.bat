@echo off

setlocal

pyinstaller ^
    --onefile ^
    --hidden-import archook ^
    --collect-data archook ^
    --hidden-import glob ^
    --hidden-import imp ^
    --hidden-import uuid ^
    --exclude-module arcpy ^
    --exclude-module numpy ^
    --additional-hooks-dir=%~dp0hooks ^
    --runtime-hook %~dp0hooks\rthooks\pyi_rth_arcpy.py ^
    --add-binary %~dp0\..\ags-service-publisher\ags_service_publisher\resources\arcgis\projects\blank\blank.aprx;ags_service_publisher/resources/arcgis/projects/blank ^
    --noupx ^
    --clean ^
    --noconsole ^
    --distpath %~dp0dist ^
    --workpath %~dp0build ^
    --specpath %~dp0 ^
    -n ags_service_publisher_gui_pro ^
    %~dp0src\main.pyw
