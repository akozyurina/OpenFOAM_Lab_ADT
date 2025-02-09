import os
import subprocess
from PyFoam.Execution.BasicRunner import BasicRunner

# Получение пути к текущей директории (где находится скрипт)
current_directory = os.path.dirname(os.path.abspath(__file__))

# Путь к вашему проекту
case_path = os.path.join(current_directory, "..", "sourses")  # Измените относительный путь при необходимости

# Количество процессоров
num_processors = 4

# Команда для запуска солвера
command = [
    "mpirun", "--oversubscribe", "-np", str(num_processors),
    "icoFoam", "-parallel", "-case", case_path
]

# Запуск процесса
process = subprocess.Popen(
    command,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

# Чтение вывода в реальном времени
for line in process.stdout:
    print(line.strip())

# Получение ошибок после завершения процесса
error_output = process.stderr.read()

# Вывод результатов
if process.returncode != 0:
    print("Ошибка во время выполнения:")
    print(error_output)
else:
    print("Симуляция успешно завершена!")