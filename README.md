### Hexlet tests and linter status:
[![Actions Status](https://github.com/A-leks-andr/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/A-leks-andr/python-project-52/actions)
### My tests and linter status:
[![My check](https://github.com/A-leks-andr/python-project-52/actions/workflows/my_check.yml/badge.svg)](https://github.com/A-leks-andr/python-project-52/actions)

[![SonarQube Cloud](https://sonarcloud.io/images/project_badges/sonarcloud-light.svg)](https://sonarcloud.io/summary/new_code?id=A-leks-andr_python-project-52)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=A-leks-andr_python-project-52&metric=coverage)](https://sonarcloud.io/summary/new_code?id=A-leks-andr_python-project-52)

# Task Manager
Task Manager — это полнофункциональное веб-приложение на Django.
Сервис реализует базовую логику трекера задач и обеспечивает удобное управление рабочими процессами:
от создания задач до их фильтрации по статусам, исполнителям и меткам.

**Демо:** [https://python-project-52-q37n.onrender.com](https://python-project-52-q37n.onrender.com)

---

## ✅ Основные возможности

### 👥 Пользователи
- Регистрация
- Авторизация / выход
- Просмотр списка пользователей
- Редактирование и удаление (только собственный аккаунт)
- Flash-сообщения об успехах и ошибках

### Задачи

- Создание, обновление, удаление
- Назначение статуса, меток(Many-to-Many) и исполнителя
- Просмотр детальной страницы
- CRUD с проверкой прав (удалять/изменять может только автор)

### Фильтры

- Через django-filter доступны параметры:
- статус
- исполнитель
- метки
- только свои задачи

### Локализация

- 🇬🇧 English
- 🇷🇺 Russian
- Переводы хранятся по приложениям (locale/ru/LC_MESSAGES)

### Интерфейс

- Bootstrap 5 через django-bootstrap5
- Общий шаблон base.html
- Разделение шаблонов по приложениям

### Логирование ошибок

- Интеграция с Rollbar для продакшена
- В dev вывод логов в консоль

### Статика

- Whitenoise
- В продакшене — автоматическая сборка статики


## Быстрый старт ⚡

### Установка
```bash
# 1. Клонировать репозиторий
git clone https://github.com/A-leks-andr/python-project-52.git
cd python-project-52