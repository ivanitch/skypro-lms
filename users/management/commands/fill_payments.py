from decimal import Decimal
from random import choice, randint

from django.core.management.base import BaseCommand
from django.utils import timezone

from lms.models import Course, Lesson
from users.models import User, Payment


class Command(BaseCommand):
    help = 'Заполняет таблицу Payment тестовыми данными'

    def handle(self, *args, **options):
        users = list(User.objects.all())
        courses = list(Course.objects.all())
        lessons = list(Lesson.objects.all())

        if not users or not courses:
            self.stdout.write(self.style.ERROR('Нет пользователей или курсов!'))
            return

        Payment.objects.all().delete()  # очищаем перед заполнением

        payment_methods = ['cash', 'transfer']

        for i in range(15):  # создаём 15 платежей
            user = choice(users)
            amount = Decimal(randint(5000, 50000))

            # 70% шанс — платёж за курс, 30% — за урок
            if randint(1, 10) <= 7 and courses:
                paid_course = choice(courses)
                paid_lesson = None
            else:
                paid_course = None
                paid_lesson = choice(lessons) if lessons else None

            Payment.objects.create(
                user=user,
                paid_course=paid_course,
                paid_lesson=paid_lesson,
                amount=amount,
                payment_method=choice(payment_methods),
                payment_date=timezone.now()
            )

        self.stdout.write(self.style.SUCCESS('Успешно создано 15 тестовых платежей!'))
