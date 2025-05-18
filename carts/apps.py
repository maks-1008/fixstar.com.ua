from django.apps import AppConfig


class CartsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "carts"
    # Видаляємо verbose_name, щоб не створювати окрему категорію в адмін-панелі

    def ready(self):
        """
        Змінюємо app_label моделі Cart, щоб вона відображалась у розділі "Замовлення" в адмін-панелі.
        Це дозволяє згрупувати всі пов'язані з замовленнями моделі в одному місці.
        """
        # Використовуємо import всередині методу, щоб уникнути циклічних імпортів
        from carts.models import Cart

        Cart._meta.app_label = "orders"
