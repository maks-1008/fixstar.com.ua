import os
from celery import Celery
from celery.schedules import crontab

# Установка переменной окружения для настроек проекта
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

app = Celery("app")

# Использовать настройки из файла settings.py с префиксом CELERY_
app.config_from_object("django.conf:settings", namespace="CELERY")

# Автоматически находить задачи (tasks) в приложениях Django
app.autodiscover_tasks()

# Настройка периодических задач
app.conf.beat_schedule = {
    "cleanup-expired-carts": {
        "task": "carts.tasks.cleanup_expired_carts",
        "schedule": crontab(hour="0", minute="0"),  # Запускать каждый день в полночь
        "args": (),
    },
}


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
