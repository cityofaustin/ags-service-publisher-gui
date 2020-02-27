@echo off

setlocal EnableDelayedExpansion
echo Converting UIC files in %~dp0src to Python modules...
for /R %~dp0src %%F IN (*.ui) do (
    set "output=%%~dpnF"
    set "output=!output!_ui.py"
    echo Converting %%F to !output!
    pyuic5.exe %%F -o !output!
    if !errorlevel! neq 0 (
        exit /b 1
    )
)
