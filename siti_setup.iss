[Setup]
AppName=Siti Desktop Pet
AppVersion=1.0.0
AppPublisher=Luqman
DefaultDirName={autopf}\Siti Desktop Pet
DefaultGroupName=Siti Desktop Pet
OutputDir=Output_Installer
OutputBaseFilename=Siti_DesktopPet_Setup_v1.0
Compression=lzma
SolidCompression=yes
PrivilegesRequired=lowest

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; Mengambil seluruh file dari folder hasil build PyInstaller
Source: "dist\main\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\Siti Desktop Pet"; Filename: "{app}\main.exe"
Name: "{group}\Uninstall Siti Desktop Pet"; Filename: "{uninstallexe}"
Name: "{autodesktop}\Siti Desktop Pet"; Filename: "{app}\main.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\main.exe"; Description: "{cm:LaunchProgram,Siti Desktop Pet}"; Flags: nowait postinstall skipifsilent