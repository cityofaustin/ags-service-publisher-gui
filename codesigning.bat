@echo off

if defined AGSSPGUICERTSHA1 if defined AGSSPGUITIMESTAMPURL (
    signtool ^
        sign ^
        /debug ^
        /sm ^
        /sha1 %AGSSPGUICERTSHA1% ^
        /fd SHA256 ^
        /tr %AGSSPGUITIMESTAMPURL% ^
        /td SHA256 ^
        %~dp0dist\ags_service_publisher_gui_pro.exe
)
