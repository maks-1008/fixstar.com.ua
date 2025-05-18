from celery import shared_task
from django.utils import timezone
from datetime import timedelta
import logging
from django.core.management import call_command

logger = logging.getLogger(__name__)


@shared_task
def cleanup_expired_carts():
    """
    Задача для очистки устаревших корзин пользователей через 48 часов после создания
    """
    # Вызывает management команду для очистки корзин
    call_command("cleanup_carts")
    return True
