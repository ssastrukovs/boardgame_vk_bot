# Установка пути к venv, файлу с требованиями и скрипту
$venvPath = ".\venv"
$requirementsFile = ".\requirements.txt"
$scriptToRun = ".\bgfridaybot.py"
$argsFile = ".\envargs.txt"

# Проверка наличия папки venv и её создание
if (-Not (Test-Path $venvPath)) {
    Write-Host "Creating Venv..."
    python -m venv $venvPath

    # Установка зависимостей
    Write-Host "Setting up requirements.txt..."
    & "$venvPath\Scripts\pip.exe" install -r $requirementsFile
}

# Проверка наличия файла envargs.txt
if (-Not (Test-Path $argsFile)) {
    Write-Host "envargs.txt Not found. Creating new one"
    New-Item -Path $argsFile -ItemType File
    Write-Host "Please fill envargs.txt with necessary arguments."
    Read-Host "Press any key to exit"
    exit
}

# Проверка, что envargs.txt не пустой
$argsContent = Get-Content $argsFile
if ([string]::IsNullOrWhiteSpace($argsContent)) {
    Write-Host "Please fill envargs.txt with necessary arguments."
    Read-Host "Press any key to exit"
    exit
}

# Преобразование аргументов в массив (каждая строка/аргумент отдельно)
$argsArray = $argsContent -split ' '

# Активация виртуального окружения
Write-Host "Venv activating..."
& "$venvPath\Scripts\Activate.ps1"

# Запуск скрипта с аргументами из файла
Write-Host "Launching $scriptToRun with args from $argsFile..."
python $scriptToRun $argsArray

# Ожидание нажатия клавиши перед выходом
Read-Host "Press any key to exit"
