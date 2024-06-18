## donation control

### Описание
Приложение для учета сбора донатов на различные целевые проекты.

### Технологии

- Python 3.9.13
- FastAPI 0.78
- SQLAlchemy 1.4
- Alembic 1.7
- Pydantic 1.9
- Google Sheets API


### Как запустить проект:


Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:Ivan-Edokov/donat-control.git
```

```
cd QRkot_spreadsheets/
```

Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Применить миграции:

```
alembic upgrade head
```

Создайте и заполните файл .env, в качестве примера используйте файл .env.example

Запустить проект:

```
uvicorn app.main:app
```

При режиме разработки можно использовать команду запуска сервера с автоматическим перезапуском

```
uvicorn app.main:app --reload
```

###  Документация API

- Загрузите файл `openapi.json` на сервисе [Redocly](https://redocly.github.io/redoc/)

### Документация API  при работающем сервере
- [Swagger](http://127.0.0.1:8000/docs)
- [Redoc](http://127.0.0.1:8000/redoc)

### Автор
[Иван Едоков](https://github.com/Ivan-Edokov)