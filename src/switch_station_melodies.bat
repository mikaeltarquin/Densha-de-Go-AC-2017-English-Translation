@echo off
:MENU
cls
echo Densha de Go!! AC 2017 English Translation - Station Melody Switcher
echo.
echo First, select your speaker configuration:
echo 0. Exit without changes
echo 1. Stereo (Recommended for most setups)
echo 2. Surround Sound (Experimental, for DX cabs)
echo.

:SPEAKER_PROMPT
set /p SPEAKER_CHOICE="Enter your speaker choice (0-2): "

if "%SPEAKER_CHOICE%"=="1" goto MUSIC_MENU
if "%SPEAKER_CHOICE%"=="2" goto MUSIC_MENU
if "%SPEAKER_CHOICE%"=="0" goto END
echo Invalid choice. Please try again.
goto SPEAKER_PROMPT

:MUSIC_MENU
cls
echo Speaker configuration selected. Now choose which station departure melody set to use:
echo 0. Go back to speaker selection
echo 1. Default (new Kanda and Ikebukuro melodies)
echo 2. Classic (pre-2023 melodies)
echo 3. Modern (new Tokyo/Shinjuku, Kanda, and Ikebukuro melodies)
echo 4. No Melodies (default door bell sound only)
echo.

:MUSIC_PROMPT
set /p MUSIC_CHOICE="Enter your melody choice (0-4): "

if "%MUSIC_CHOICE%"=="1" goto SWITCH
if "%MUSIC_CHOICE%"=="2" goto SWITCH
if "%MUSIC_CHOICE%"=="3" goto SWITCH
if "%MUSIC_CHOICE%"=="4" goto SWITCH
if "%MUSIC_CHOICE%"=="0" goto MENU
echo Invalid choice. Please try again.
goto MUSIC_PROMPT

:SWITCH
set "SCRIPT_DIR=%~dp0"
set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"
English_Mod_Tool_-_DO_NOT_DELETE.exe switch_music "%SCRIPT_DIR%" "%SCRIPT_DIR%\patches" %SPEAKER_CHOICE% %MUSIC_CHOICE%
if errorlevel 1 (
    echo.
    echo Failed to switch station melodies.
    pause
    goto MENU
)

echo.
echo Station melodies changed successfully!
echo Press any key to exit...
pause >nul
exit /b 0

:END
echo.
echo Exiting without changes.
echo Press any key to exit...
pause >nul
exit /b 0