# Skypro LMS - Онлайн образовательная система

Бэкенд-часть образовательной платформы (LMS), разработанная на базе **Django 6** и **Django REST Framework (DRF)**.
Система предоставляет API для управления курсами, уроками и профилями пользователей.

## Cтек

* **Python:** 3.12+
* **Фреймворк:** Django 6.0
* **API:** Django REST Framework (DRF)
* **База данных:** PostgreSQL
* **Менеджер пакетов и окружений:** `uv`

## Функционал

1. **Приложение `users` (Управление пользователями):**
    * Кастомная модель пользователя унаследована от `AbstractBaseUser`.
    * Авторизация реализована через Email (поле `username` удалено).
    * Добавлены дополнительные поля: `phone`, `city`, `avatar`.
    * Разработан эндпоинт для редактирования профиля пользователя (через `RetrieveUpdateAPIView`).

2. **Приложение `lms` (Учебные материалы):**
    * Модели `Course` (Курс) и `Lesson` (Урок) со связью "один-ко-многим".
    * CRUD API для сущности "Курс" реализован с использованием `ViewSets`.
    * CRUD API для сущности "Урок" реализован через `Generic` классы.
    * Настроены базовые сериализаторы для корректного отображения и валидации данных.

## Установка и запуск проекта

Подготовка окружения

Склонируйте репозиторий на локальную машину:

```bash
git clone git@github.com:ivanitch/skypro-lms.git skypro-lms
cd skypro-lms
```

Скопировать файл конфигурации

```bash
cp .env.example .env
```

Для управления зависимостями и виртуальным окружением используется uv. Синхронизируйте проект:

```bash
uv sync
```

Миграции

```bash
uv run python manage.py makemigrations
uv run python manage.py migrate
```

Создать супер-пользователя

```bash
uv run python manage.py createsuperuser
```

Запустите локальный сервер:

```bash
uv run python manage.py runserver
```

## Доступные эндпоинты API

Пользователи:

    GET, PUT, PATCH /users/profile/<id>/ - Просмотр и редактирование профиля.

Курсы (ViewSet):

    GET /courses/ - Список курсов.

    POST /courses/ - Создание курса.

    GET /courses/<id>/ - Детальная информация о курсе (включая привязанные уроки).

    PUT, PATCH /courses/<id>/ - Обновление курса.

    DELETE /courses/<id>/ - Удаление курса.

Уроки (Generics):

    GET /lessons/ - Список уроков.

    POST /lessons/create/ - Создание нового урока.

    GET /lessons/<id>/ - Детальная информация об уроке.

    PUT, PATCH /lessons/<id>/update/ - Обновление урока.

    DELETE lessons/<id>/delete/ - Удаление урока.
