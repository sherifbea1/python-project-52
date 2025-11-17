### Hexlet tests and linter status
[![Actions Status](https://github.com/sherifbea1/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/sherifbea1/python-project-52/actions)
![Main workflow](https://github.com/sherifbea1/python-project-52/actions/workflows/main.yml/badge.svg)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=sherifbea1_python-project-52&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=sherifbea1_python-project-52)

---

### Render
Приложение задеплоено на Render:  
https://python-project-52-7hde.onrender.com

---

## Описание

**Task Manager** — веб-приложение для управления задачами.

Возможности:
- регистрация и аутентификация пользователей
- CRUD для пользователей, статусов, задач и меток  
- невозможность удаления связанных сущностей  
- фильтрация задач по:
  - статусу  
  - исполнителю  
  - метке  
  - задачам, созданным текущим пользователем  
- логирование ошибок через **Rollbar**
- автоматическая проверка кода через **GitHub Actions**
- анализ качества и покрытия тестами через **SonarCloud**

---

## Технологии
- Python 3.10+
- Django
- PostgreSQL / SQLite
- Bootstrap 5
- GitHub Actions
- SonarCloud
- Rollbar

---

## Локальный запуск
make install
make migrate
make run
