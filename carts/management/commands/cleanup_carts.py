from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import logging

from carts.models import Cart

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Очищает корзины пользователей, которые не были оформлены в течение 48 часов"

    def handle(self, *args, **options):
        # Определяем время, старше которого корзины должны быть удалены (48 часов назад)
        expiration_time = timezone.now() - timedelta(hours=48)

        # Выбираем корзины, созданные более 48 часов назад
        expired_carts = Cart.objects.filter(
            created_timestamp__lt=expiration_time,
            user__isnull=False,  # Только для зарегистрированных пользователей
        )

        # Проверяем наличие корзин для удаления
        count = expired_carts.count()

        if count > 0:
            # Сохраняем информацию о том, что будут удалены
            logger.info(
                f"Удаляем {count} устаревших корзин, созданных до {expiration_time}"
            )

            # Удаляем устаревшие корзины
            result = expired_carts.delete()

            # Выводим информацию о результате
            self.stdout.write(
                self.style.SUCCESS(f"Успешно удалено {count} устаревших корзин")
            )
        else:
            self.stdout.write(self.style.SUCCESS("Нет устаревших корзин для удаления"))
