from celery import shared_task
from django.conf import settings
from django.core.mail import send_mass_mail

from lms.models import Course, Subscription


@shared_task
def send_course_update_email(course_id: int):
    """
    Отправляет уведомление об обновлении курса всем подписчикам батчем.
    """
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return

    # Получаем email-адреса всех пользователей, подписанных на этот курс
    subscriptions = Subscription.objects.filter(course=course).select_related('user')
    recipient_emails = [sub.user.email for sub in subscriptions if sub.user.email]

    if not recipient_emails:
        return

    subject = f'Обновление курса "{course.title}"'
    message = f'Здравствуйте!\nМатериалы курса "{course.title}" были обновлены.'
    from_email = settings.DEFAULT_FROM_EMAIL

    # Формируем кортеж сообщений для пакета (batch)
    datatuple = (
        (subject, message, from_email, [email])
        for email in recipient_emails
    )

    # Отправка батчем через одно SMTP-соединение
    send_mass_mail(datatuple, fail_silently=False)
