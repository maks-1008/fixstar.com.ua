from django.contrib import admin
from django.apps import apps


def customize_admin():
    """
    Настройка админ-панели Django.
    Эта функция должна вызываться после загрузки всех приложений.
    """
    # Переименование стандартных заголовков в админке
    admin.site.site_header = "Адміністрування сайту"
    admin.site.site_title = "Адміністрування"
    admin.site.index_title = "Головна"
