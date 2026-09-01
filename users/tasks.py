from datetime import timedelta

from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


@shared_task
def check_inactive_users():
    """
    Блокирует пользователей, которые не заходили в систему более 30 дней.
    """
    today = timezone.now()
    one_month_ago = today - timedelta(days=30)

    # Находим активных пользователей, у которых last_login был более 30 дней назад
    inactive_users = User.objects.filter(
        is_active=True,
        last_login__lte=one_month_ago
    )

    # Пакетный апдейт (bulk update)
    updated_count = inactive_users.update(is_active=False)
    return f"Заблокировано пользователей по неактивности: {updated_count}"
