import requests
import os
from pathlib import Path

# Проверяем физическое наличие файла
file_path = Path('media/product_images/DIN933.webp')
if file_path.exists():
    print(f"Файл существует локально: {file_path}")
    print(f"Размер файла: {file_path.stat().st_size} байт")
else:
    print(f"Файл не найден локально: {file_path}")
    
# Пробуем получить файл через HTTP
url = "http://127.0.0.1:8000/media/product_images/DIN933.webp"
try:
    response = requests.get(url, timeout=5)
    print(f"\nHTTP запрос к {url}")
    print(f"Статус ответа: {response.status_code}")
    print(f"Тип контента: {response.headers.get('Content-Type')}")
    print(f"Размер ответа: {len(response.content)} байт")
except Exception as e:
    print(f"Ошибка при запросе: {e}")

# Проверяем конфигурацию URL для медиа в Django
print("\nПроверка URL конфигурации:")
if os.path.exists('app/urls.py'):
    with open('app/urls.py', 'r', encoding='utf-8') as f:
        urls_content = f.read()
    
    # Ищем строки, относящиеся к настройке медиа-URL
    for line in urls_content.split('\n'):
        if 'MEDIA_URL' in line or 'MEDIA_ROOT' in line or 'static(' in line:
            print(f"  {line.strip()}")
            
    # Проверяем, есть ли urlpatterns += static(...) в файле
    if "static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)" in urls_content:
        print("  [OK] Найдена правильная настройка для обработки медиа-файлов")
    else:
        print("  [ОШИБКА] Не найдена настройка для обработки медиа-файлов")
        
# Проверяем, импортируется ли static в urls.py
if os.path.exists('app/urls.py'):
    with open('app/urls.py', 'r', encoding='utf-8') as f:
        for i, line in enumerate(f.readlines()):
            if 'from django.conf.urls.static import static' in line:
                print(f"  [OK] Найден импорт static в строке {i+1}")
                break
        else:
            print("  [ОШИБКА] Не найден импорт static в urls.py") 