@echo off
REM Step 1: Delete the existing patches folder
echo Deleting existing patches folder...
rmdir /s /q "D:\DenshaProject\__installer\patches"

REM Step 2: Re-create the patches folder using create_patches.py
echo Re-creating patches folder...
python create_patches.py

REM Step 3: Create a new installer .exe from installer.py
echo Creating new installer executable...
pyinstaller --onefile --distpath "D:\DenshaProject\__installer" --workpath "D:\DenshaProject\__installer\build" "D:\DenshaProject\__installer\English_Mod_Tool_-_DO_NOT_DELETE.py"

REM Step4: Compile the Inno Setup script to generate a new release
echo Compiling the Inno Setup script...
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" "D:\DenshaProject\__installer\release_setup.iss"

echo Process completed successfully!
pause