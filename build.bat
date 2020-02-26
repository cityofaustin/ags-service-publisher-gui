@echo off

setlocal

call "%~dp0buildtemplates.bat"

pyinstaller ^
    --onefile ^
    --hidden-import glob ^
    --hidden-import uuid ^
    --hidden-import imp ^
    --exclude-module arcpy ^
    --exclude-module numpy ^
    --exclude-module PySide2.QtHelp ^
    --exclude-module PySide2.QtMultimedia ^
    --exclude-module PySide2.QtNetwork ^
    --exclude-module PySide2.QtOpenGL ^
    --exclude-module PySide2.QtPrintSupport ^
    --exclude-module PySide2.QtQml ^
    --exclude-module PySide2.QtQuick ^
    --exclude-module PySide2.QtQuickWidgets ^
    --exclude-module PySide2.QtScript ^
    --exclude-module PySide2.QtSensors ^
    --exclude-module PySide2.QtSerialPort ^
    --exclude-module PySide2.QtSql ^
    --exclude-module PySide2.QtSvg ^
    --exclude-module PySide2.QtTest ^
    --exclude-module PySide2.QtWebEngineWidgets ^
    --exclude-module PySide2.QtWebKit ^
    --exclude-module PySide2.QtWebKitWidgets ^
    --exclude-module PySide2.QtXml ^
    --exclude-module PySide2.Qwt5 ^
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
