import os
import sys
import django
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Настраиваем Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
django.setup()

from django.conf import settings

# Получаем данные подключения из настроек Django
db_settings = settings.DATABASES["default"]

# Устанавливаем соединение с PostgreSQL
print("Подключение к базе данных PostgreSQL...")
conn = psycopg2.connect(
    dbname=db_settings["NAME"],
    user=db_settings["USER"],
    password=db_settings["PASSWORD"],
    host=db_settings["HOST"],
    port=db_settings["PORT"],
)

# Устанавливаем уровень изоляции транзакций
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

# Создаем курсор
cur = conn.cursor()

# Проверяем существование таблицы
print("Проверка существования таблицы orders_emailnotificationsettings...")
cur.execute(
    """
    SELECT EXISTS (
        SELECT FROM information_schema.tables 
        WHERE table_name = 'orders_emailnotificationsettings'
    );
"""
)
table_exists = cur.fetchone()[0]

if not table_exists:
    print(
        "Таблица orders_emailnotificationsettings не существует. Ничего не нужно делать."
    )
else:
    print("Таблица orders_emailnotificationsettings существует. Проверяем структуру...")

    # Проверяем наличие столбца name
    cur.execute(
        """
        SELECT EXISTS (
            SELECT FROM information_schema.columns 
            WHERE table_name = 'orders_emailnotificationsettings' AND column_name = 'name'
        );
    """
    )
    name_exists = cur.fetchone()[0]

    if name_exists:
        print("Столбец 'name' уже существует. Ничего не нужно делать.")
    else:
        print("Столбец 'name' отсутствует. Добавляем его...")

        # Добавляем столбец name
        cur.execute(
            """
            ALTER TABLE orders_emailnotificationsettings 
            ADD COLUMN name VARCHAR(100) NOT NULL DEFAULT 'Основний';
        """
        )
        print("Столбец 'name' успешно добавлен.")

    # Проверяем тип столбца email
    cur.execute(
        """
        SELECT data_type 
        FROM information_schema.columns 
        WHERE table_name = 'orders_emailnotificationsettings' AND column_name = 'email';
    """
    )
    email_type = cur.fetchone()[0]

    if email_type.lower() == "text":
        print("Столбец 'email' уже имеет тип TEXT. Ничего не нужно делать.")
    else:
        print(f"Столбец 'email' имеет тип {email_type}. Изменяем на TEXT...")

        # Изменяем тип столбца email на TEXT
        cur.execute(
            """
            ALTER TABLE orders_emailnotificationsettings 
            ALTER COLUMN email TYPE TEXT;
        """
        )
        print("Тип столбца 'email' успешно изменен на TEXT.")

print("Выполнение скрипта завершено успешно.")

# Закрываем курсор и соединение
cur.close()
conn.close()
