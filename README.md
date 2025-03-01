# Совместный проект с разработчиками

Работа представляет собой backend-часть для сайта объявлений. 

Содержит 3 приложения: advert, feedback и user, фикстуры для тестирования.

### Реализованный функционал:

- Авторизация и аутентификация пользователей.
- Распределение ролей между пользователями (пользователь и админ).
- Восстановление пароля через электронную почту.
- CRUD для объявлений на сайте (админ может удалять или редактировать все объявления, а пользователи только свои).
- Под каждым объявлением пользователи могут оставлять отзывы.
- В заголовке сайта можно осуществлять поиск объявлений по названию.

### Стек технологий:

- Django Rest Framework
- PostgreSQL
- drf-yasg
- requests
- djoser
- django-filter
- rest-framework-simplejwt
- flake8

### Инструкция по запуску:
- Сделать fork этого проекта к себе в репозиторий
- В PyCharm через интерфейс открыть меню git, нажать clone, указать url вашего репозитория
- Установить зависимости командой `pip install -r requirements.txt`
- Провести миграции командой `python manage.py migrate`
- Загрузить фикстуры через команду `python manage.py loaddata fixtures/{fixture_name}.json`
- Запустить локальный сервер командой `python manage.py runserver`
