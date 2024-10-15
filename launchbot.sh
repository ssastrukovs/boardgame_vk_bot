#!/bin/bash

# Установка путей к виртуальному окружению, файлу с зависимостями и Python-скрипту
venv_dir="./venv"
requirements_file="./requirements.txt"
script_to_run="./bgfridaybot.py"
args_file="./envargs.txt"

# Проверка наличия папки venv и её создание
if [ ! -d "$venv_dir" ]; then
    echo "Создание виртуального окружения..."
    python3 -m venv "$venv_dir"

    # Установка зависимостей
    echo "Установка зависимостей из requirements.txt..."
    "$venv_dir/bin/pip" install -r "$requirements_file"
fi

# Проверка наличия файла envargs.txt
if [ ! -f "$args_file" ]; then
    echo "Файл envargs.txt не найден. Создание пустого файла..."
    touch "$args_file"
    echo "Please fill envargs.txt with necessary arguments."
    read -n 1 -s -r -p "Нажмите любую клавишу, чтобы выйти"
    echo
    exit 1
fi

# Проверка, что envargs.txt не пустой
args_content=$(<"$args_file")
if [ -z "$args_content" ]; then
    echo "Файл envargs.txt пуст. Please fill envargs.txt with necessary arguments."
    read -n 1 -s -r -p "Нажмите любую клавишу, чтобы выйти"
    echo
    exit 1
fi

# Активация виртуального окружения
echo "Активация виртуального окружения..."
source "$venv_dir/bin/activate"

# Запуск скрипта с аргументами из файла
echo "Запуск $script_to_run с аргументами из $args_file..."
python3 "$script_to_run" $args_content

# Ожидание нажатия клавиши перед выходом
read -n 1 -s -r -p "Нажмите любую клавишу, чтобы выйти"
echo
