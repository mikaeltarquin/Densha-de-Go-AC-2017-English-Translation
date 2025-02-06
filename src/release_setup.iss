#define CurrentDate GetDateTimeString('yymmdd', '-', '-')
#define MyAppName "Densha de Go!! AC 2017 English Translation"
#define MyAppVersion "5.80.02-en" + CurrentDate
#define MyAppPublisher "MikaelTarquin"

[Setup]
AppName={#MyAppName}
AppVersion={#MyAppVersion}
DefaultDirName=C:\
OutputDir=released_exe
OutputBaseFilename=tg4ac_{#MyAppVersion}
AppPublisher={#MyAppPublisher}
DisableProgramGroupPage=yes

; Force directory selection
DisableDirPage=no
AlwaysShowDirOnReadyPage=yes
CreateAppDir=yes
UsePreviousAppDir=yes

; Disable automatic next page
DisableReadyPage=no
DisableReadyMemo=no

[Types]
Name: "full"; Description: "Full installation"

[Components]
Name: "main"; Description: "Main Files"; Types: full; Flags: fixed

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop icon"; GroupDescription: "Additional icons:"

[Code]
var
  DirPage: TWizardPage;

procedure InitializeWizard;
begin
  WizardForm.DirEdit.Text := '';
  WizardForm.DirBrowseButton.Visible := True;
end;

function ShouldSkipPage(PageID: Integer): Boolean;
begin
  // Skip all pages except directory selection
  Result := (PageID = wpSelectComponents) or 
            (PageID = wpSelectTasks) or 
            (PageID = wpReady);
end;

function NextButtonClick(CurPageID: Integer): Boolean;
begin
  Result := True;
  
  if CurPageID = wpSelectDir then
  begin
    if not FileExists(WizardDirValue + '\TG4AC\Binaries\Win64\TG4AC-Win64-Shipping.exe') then
    begin
      MsgBox('Please select the folder where Densha de Go!! AC 2017 is installed.' + #13#10 + 
             'This should be the folder that contains the DGOREPR, Engine, and TG4AC folders.', mbError, MB_OK);
      Result := False;
    end;
  end;
end;

[Files]
Source: "D:\DenshaProject\__installer\English_Mod_Tool_-_DO_NOT_DELETE.exe"; DestDir: "{app}"
Source: "D:\DenshaProject\__installer\xdelta3.exe"; DestDir: "{app}"; Flags: deleteafterinstall
Source: "D:\DenshaProject\__installer\English_Mod_README.MD"; DestDir: "{app}"
Source: "D:\DenshaProject\__installer\patches\*"; DestDir: "{app}\patches"; Flags: recursesubdirs createallsubdirs deleteafterinstall

[Messages]
SelectDirDesc=Where is Densha de Go!! AC 2017 installed?
SelectDirLabel3=Please select the folder where Densha de Go!! AC 2017 is installed. This should be the folder that contains the DGOREPR, Engine, and TG4AC folders. **NOTICE** If you use the Browse button, make sure to MANUALLY DELETE the additional "New Folder" that is automatically added to the path in the text box below!
WizardSelectDir=Select Game Location. 
SelectDirBrowseLabel=To continue, click Next, and press YES when warned that the folder already exists. If you would like to select a different folder, click Browse.

[Run]
Filename: "{app}\English_Mod_Tool_-_DO_NOT_DELETE.exe"; Parameters: "install ""{app}"" ""{app}\patches"""; StatusMsg: "Installing English Translation..."; Flags: waituntilterminated

[UninstallRun]
Filename: "{app}\English_Mod_Tool_-_DO_NOT_DELETE.exe"; Parameters: "restore ""{app}"" ""{app}\patches"""; StatusMsg: "Restoring Original Files..."; Flags: waituntilterminated

[UninstallDelete]
Type: files; Name: "{app}\English_Mod_Tool_-_DO_NOT_DELETE.exe"
Type: files; Name: "{app}\xdelta3.exe"
Type: files; Name: "{app}\English_Mod_README.MD"
Type: filesandordirs; Name: "{app}\patches"