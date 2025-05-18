import os
from pathlib import Path

print("Начало проверки")

# Проверяем наличие файла
file_path = Path('media/product_images/DIN933.webp')
print(f"Файл существует: {file_path.exists()}")

# Проверяем содержимое директории
print("\nСодержимое директории media/product_images:")
try:
    for item in os.listdir('media/product_images'):
        print(f" - {item}")
except Exception as e:
    print(f"Ошибка при чтении директории: {e}")

print("Проверка завершена") 