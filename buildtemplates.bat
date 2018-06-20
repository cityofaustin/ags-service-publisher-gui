@echo off

setlocal EnableDelayedExpansion

echo Converting UIC files in %cd% to Python modules...
for /R %%F IN (*.ui) do (
    set "output=%%~dpnF"
    set "output=!output!_ui.py"
    echo Converting %%F to !output!
    pyside2-uic.exe %%F -o !output!
)
