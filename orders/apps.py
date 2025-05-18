from django.apps import AppConfig


class OrdersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "orders"
    verbose_name = "Замовлення"

    def ready(self):
        # Импортируем сигналы при загрузке приложения
        import orders.signals
