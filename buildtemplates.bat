@echo off

setlocal EnableDelayedExpansion

for /f %%F in ('where python') do SET PYTHONDIR=%%~dpF

echo Converting UIC files in %cd% to Python modules...
for /R %%F IN (*.ui) do (
    set "output=%%~dpnF"
    set "output=!output!.py"
    echo Converting %%F to !output!
    call "!PYTHONDIR!\Lib\site-packages\PyQt4\pyuic4.bat" %%F -o !output!
)
