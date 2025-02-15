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

[Files]
Source: "D:\DenshaProject\__installer\English_Mod_Tool_-_DO_NOT_DELETE.exe"; DestDir: "{app}"
Source: "D:\DenshaProject\__installer\xdelta3.exe"; DestDir: "{app}";
Source: "D:\DenshaProject\__installer\English_Mod_README.MD"; DestDir: "{app}"
; Install music patches (keep these for the switcher)
Source: "D:\DenshaProject\__installer\patches\music\*"; DestDir: "{app}\patches\music"; Flags: recursesubdirs createallsubdirs
; Install other patches (delete after installation)
Source: "D:\DenshaProject\__installer\patches\*"; DestDir: "{app}\patches"; Excludes: "music\*"; Flags: recursesubdirs createallsubdirs deleteafterinstall
; Add music switcher batch file
Source: "D:\DenshaProject\__installer\switch_station_melodies.bat"; DestDir: "{app}"

[Code]
var
  SpeakerPage: TWizardPage;
  MusicPage: TWizardPage;
  SpeakerButtons: array[1..2] of TRadioButton;
  MusicButtons: array[1..4] of TRadioButton;
  SpeakerDesc: TNewStaticText;

// Update function to get both choices
function GetChoices(Param: string): string;
var
  i: Integer;
  speakerChoice, musicChoice: string;
begin
  // Get speaker choice
  for i := 1 to 2 do
  begin
    if SpeakerButtons[i].Checked then
    begin
      speakerChoice := IntToStr(i);
      break;
    end;
  end;
  
  // Get music choice
  for i := 1 to 4 do
  begin
    if MusicButtons[i].Checked then
    begin
      musicChoice := IntToStr(i);
      break;
    end;
  end;
  
  Result := speakerChoice + ' ' + musicChoice;
end;

procedure InitializeWizard;
begin
  WizardForm.DirEdit.Text := '';
  WizardForm.DirBrowseButton.Visible := True;

  // Create speaker selection page
  SpeakerPage := CreateCustomPage(wpSelectDir, 'Speaker Configuration', 
    'Choose your speaker configuration.');

  // Create radio buttons for speaker options
  SpeakerButtons[1] := TRadioButton.Create(SpeakerPage);
  SpeakerButtons[1].Parent := SpeakerPage.Surface;
  SpeakerButtons[1].Caption := 'Stereo (Recommended for most setups)';
  SpeakerButtons[1].Left := 0;
  SpeakerButtons[1].Top := 0;
  SpeakerButtons[1].Width := SpeakerPage.SurfaceWidth;
  SpeakerButtons[1].Checked := True;

  SpeakerButtons[2] := TRadioButton.Create(SpeakerPage);
  SpeakerButtons[2].Parent := SpeakerPage.Surface;
  SpeakerButtons[2].Caption := 'Surround Sound (Experimental, for DX cabs)';
  SpeakerButtons[2].Left := 0;
  SpeakerButtons[2].Top := 20;
  SpeakerButtons[2].Width := SpeakerPage.SurfaceWidth;

  // Add description label for speaker options
  SpeakerDesc := TNewStaticText.Create(SpeakerPage);
  SpeakerDesc.Parent := SpeakerPage.Surface;
  SpeakerDesc.Caption := 'Note: Surround Sound option is only intended for DX cabinet setups with proper 6-channel audio support. Most users should select Stereo.';
  SpeakerDesc.Left := 0;
  SpeakerDesc.Top := 50;
  SpeakerDesc.Width := SpeakerPage.SurfaceWidth;
  SpeakerDesc.WordWrap := True;

  // Create music selection page
  MusicPage := CreateCustomPage(SpeakerPage.ID, 'Station Melody Selection', 
    'Choose which station melodies you would like to use.');

  // Create radio buttons for music options
  MusicButtons[1] := TRadioButton.Create(MusicPage);
  MusicButtons[1].Parent := MusicPage.Surface;
  MusicButtons[1].Caption := 'Default Melodies (Classic + New Kanda/Ikebukuro)';
  MusicButtons[1].Left := 0;
  MusicButtons[1].Top := 0;
  MusicButtons[1].Width := MusicPage.SurfaceWidth;
  MusicButtons[1].Checked := True;

  MusicButtons[2] := TRadioButton.Create(MusicPage);
  MusicButtons[2].Parent := MusicPage.Surface;
  MusicButtons[2].Caption := 'Classic Melodies Only';
  MusicButtons[2].Left := 0;
  MusicButtons[2].Top := 20;
  MusicButtons[2].Width := MusicPage.SurfaceWidth;

  MusicButtons[3] := TRadioButton.Create(MusicPage);
  MusicButtons[3].Parent := MusicPage.Surface;
  MusicButtons[3].Caption := 'New Tokyo/Shinjuku/Kanda/Ikebukuro Melodies';
  MusicButtons[3].Left := 0;
  MusicButtons[3].Top := 40;
  MusicButtons[3].Width := MusicPage.SurfaceWidth;

  MusicButtons[4] := TRadioButton.Create(MusicPage);
  MusicButtons[4].Parent := MusicPage.Surface;
  MusicButtons[4].Caption := 'No Melodies (Unmodified)';
  MusicButtons[4].Left := 0;
  MusicButtons[4].Top := 60;
  MusicButtons[4].Width := MusicPage.SurfaceWidth;
end;

function ShouldSkipPage(PageID: Integer): Boolean;
begin
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

[Messages]
SelectDirDesc=Where is Densha de Go!! AC 2017 installed?
SelectDirLabel3=Please select the folder where Densha de Go!! AC 2017 is installed. This should be the folder that contains the DGOREPR, Engine, and TG4AC folders. **NOTICE** If you use the Browse button, make sure to MANUALLY DELETE the additional "New Folder" that is automatically added to the path in the text box below!
WizardSelectDir=Select Game Location
SelectDirBrowseLabel=To continue, click Next, and press YES when warned that the folder already exists. If you would like to select a different folder, click Browse.

[Run]
Filename: "{app}\English_Mod_Tool_-_DO_NOT_DELETE.exe"; Parameters: "install ""{app}"" ""{app}\patches"" {code:GetChoices}"; StatusMsg: "Installing English Translation..."; Flags: waituntilterminated

[UninstallRun]
Filename: "{app}\English_Mod_Tool_-_DO_NOT_DELETE.exe"; Parameters: "restore ""{app}"" ""{app}\patches"""; StatusMsg: "Restoring Original Files..."; Flags: waituntilterminated; RunOnceId: "RestoreOriginal"

[UninstallDelete]
Type: files; Name: "{app}\English_Mod_Tool_-_DO_NOT_DELETE.exe"
Type: files; Name: "{app}\xdelta3.exe"
Type: files; Name: "{app}\English_Mod_README.MD"
Type: files; Name: "{app}\switch_station_melodies.bat"
Type: filesandordirs; Name: "{app}\patches"