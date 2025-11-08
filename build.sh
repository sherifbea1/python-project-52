#!/usr/bin/env bash
# Устанавливаем uv (ускоренный менеджер пакетов)
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

# Устанавливаем зависимости проекта
pip install -r requirements.txt

# Применяем миграции и собираем статику
python manage.py collectstatic --noinput
python manage.py migrate
