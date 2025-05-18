from django.db import connection

def install_extension():
    with connection.cursor() as cursor:
        cursor.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")
        print("Расширение pg_trgm успешно установлено")

if __name__ == "__main__":
    install_extension()