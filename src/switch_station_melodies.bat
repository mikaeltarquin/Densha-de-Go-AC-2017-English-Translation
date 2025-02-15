@echo off
:MENU
cls
echo Densha de Go!! AC 2017 English Translation - Station Melody Switcher
echo.
echo Available options:
echo 0. Exit without changes
echo 1. Default Melodies (Classic + New Kanda/Ikebukuro)
echo 2. Classic Melodies Only
echo 3. New Tokyo/Shinjuku/Kanda/Ikebukuro Melodies
echo 4. No Melodies
echo.

:PROMPT
set /p MUSIC_CHOICE="Enter your choice (0-4): "

if "%MUSIC_CHOICE%"=="0" goto END
if "%MUSIC_CHOICE%"=="1" goto SWITCH
if "%MUSIC_CHOICE%"=="2" goto SWITCH
if "%MUSIC_CHOICE%"=="3" goto SWITCH
if "%MUSIC_CHOICE%"=="4" goto SWITCH
echo Invalid choice. Please try again.
goto PROMPT

:SWITCH
set "SCRIPT_DIR=%~dp0"
set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"
English_Mod_Tool_-_DO_NOT_DELETE.exe switch_music "%SCRIPT_DIR%" "%SCRIPT_DIR%\patches" %MUSIC_CHOICE%
if errorlevel 1 (
    echo.
    echo Failed to switch station melodies.
    pause
    goto MENU
)

echo.
echo Station melodies changed successfully!
pause
goto MENU

:END
echo.
echo Exiting without changes.
pause