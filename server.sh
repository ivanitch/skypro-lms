#!/bin/bash

# Запуск
# ./server.sh
# или просто: bash server.sh

# Запускаем сервер на порту 8090
uv run python manage.py runserver 8090
