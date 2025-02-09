#!/bin/bash

# Определение пути к проекту
CASE_PATH=$(dirname "$(readlink -f "$0")")/sourses

# Удаление старых папок processor*
echo "Удаление старых временных папок processor*..."
rm -rf $CASE_PATH/processor*

# Разбиение сетки на поддомены
echo "Разбиение сетки на поддомены..."
decomposePar -case $CASE_PATH -force
if [ $? -ne 0 ]; then
    echo "Ошибка при выполнении decomposePar. Прерывание скрипта."
    exit 1
fi

# Запуск Python-скрипта для параллельной симуляции
echo "Запуск симуляции через Python..."
python3 $CASE_PATH/test_1.py
if [ $? -ne 0 ]; then
    echo "Ошибка при выполнении Python-скрипта. Прерывание скрипта."
    exit 1
fi

# Объединение результатов
echo "Объединение результатов из поддоменов..."
reconstructPar -case $CASE_PATH -latestTime
if [ $? -ne 0 ]; then
    echo "Ошибка при выполнении reconstructPar. Прерывание скрипта."
    exit 1
fi

# Удаление временных папок processor*
echo "Удаление временных папок processor*..."
rm -rf $CASE_PATH/processor*

# Открытие проекта в ParaView
echo "Открытие проекта в ParaView..."
paraFoam -case $CASE_PATH

if [ $? -ne 0 ]; then
    echo "Ошибка при открытии проекта в ParaView."
    exit 1
fi

echo "Проект успешно открыт в ParaView!"

echo "Скрипт выполнен успешно!"
