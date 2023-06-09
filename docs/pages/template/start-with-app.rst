Начинаем писать django-app
==========================

Устанави виртуальное окружение
------------------------------

Только слабаки работают без виртуального окружения.
Не будь таким - установи виртуальное окружение.

.. code-block:: bash

  >> poetry install

УдОли __CHANGEME__
-------------------

В некоторых местах кода и именах файлов вставлен __CHANGEME__.

Вставлен этот текст только для того, чтобы ты его заменил.
Найти включения __CHANGEME__ можно скриптом:

.. code-block:: bash

  >> make ready

а можно и просто поиском по тексту

- `__CHANGEME__appname` замени на имя аппы (например, nova_device)
- `__CHANGEME__projectname` замени на имя проекта (например, django_nova_device)
- `__CHANGEME__projectslug` замени на slug (например django-nova-device)
- `__CHANGEME__routerimport` замени на импорт router-a

( например, nova_device.api.nested_router import router)
- `__CHANGEME__uncomment` убрать и раскомментировать строку, включающую её
- `__CHANGEME__remove` - убрать этот текст

Начинай писать код
------------------

Код сам себя не напишет.

В проекте есть 2 очень важные папки:

- src - там должен лежать весь код создаваемой аппы

- server - там лежит код, который нужен для тестирования
  (т.к. апа не может быть запущена и, соответственно,
  протестирована без использования сервера).

Естественно: сервер не должен быть использован для прода.
Он только для тестов.

Так где писать код-то?
-----------------------

- Создай папку в ./src/ с подходящим для своего апа названием.

Например: my_django_app

- создавай там все, что обычно создают во время написания аппы:

apps.py, admin.py, models, api и т.д.

- ТЕСТЫ клади в папку ./tests/ (рядом с src, а не в неё)

Как тестировать код
-------------------

Тестируется код через сервер (папка server) таким образом:

- poetry run pytest .

Для всех проверок из ci есть make команды (начинаются с "ci-").
