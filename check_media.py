import os
from pathlib import Path

# Проверяем наличие и доступность файла
file_path = Path('media/product_images/DIN933.webp')
print(f"Файл существует: {file_path.exists()}")
if file_path.exists():
    print(f"Размер файла: {file_path.stat().st_size} байт")
    print(f"Права доступа: {oct(file_path.stat().st_mode)}")

# Выводим список всех файлов в папке
print("\nСписок файлов в папке media/product_images:")
for file in Path('media/product_images').glob('*'):
    print(f" - {file.name} ({file.stat().st_size} bytes)")

# Проверяем настройки Django
if os.path.exists('app/settings.py'):
    print("\nНастройки Django:")
    with open('app/settings.py', 'r', encoding='utf-8') as f:
        settings_content = f.read()
        
    # Извлекаем и выводим настройки MEDIA_URL и MEDIA_ROOT
    if 'MEDIA_URL' in settings_content:
        for line in settings_content.split('\n'):
            if 'MEDIA_URL' in line or 'MEDIA_ROOT' in line:
                print(line.strip()) 