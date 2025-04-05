# PAVEPO TZ
### Описание
Реализовать сервис по загрузке аудио-файлов от пользователей, используя FastAPI, SQLAlchemy и Docker. Пользователи могут давать файлам имя в самом API.
Файлы хранить локально, хранилище использовать не нужно.
Использовать асинхронный код.
БД - PostgreSQL 16.

Ожидаемый результат:
1. Готовое API с возможностью авторизации с последующей аутентификацией к запросам через внутренние токены API.
2. Документация по развертыванию сервиса и БД в Docker.
### Технологии
- Python 3.10
- Aiogram
- FastAPI
- Pydantic
- SQLAlchemy
- Uvicorn
- AuthX
### Запуск проекта в dev-режиме
- Установите и активируйте виртуальное окружение
```
python -m venv venv
sourse venv/Scripts/activate
```
- Установите зависимости из файла requirements.txt
```
pip install -r requirements.txt
``` 
- Выполните команду:
```
docker build -t app .
docker run app
```
### Автор
Артём Карташян
#### (https://github.com/yhtrg)