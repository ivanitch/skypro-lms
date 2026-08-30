import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')
# Загрузка настроек из settings.py с префиксом CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')
# Автоматический поиск задач в файлах tasks.py всех приложений
app.autodiscover_tasks()
