### Описание проекта:

Cайт Foodgram, «Продуктовый помощник». 
На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.
 
### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:ifyoumasha/foodgram-project-react.git
```

```
cd foodgram-project-react
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
или
python -m venv venv
```

```
. venv/bin/activate
или
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
или
python manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
или
python manage.py runserver
```

### Как запустить документацию:

1. Открыть приложение Docker

2. Перейти в директорию infra:

```
cd infra
```

3. Запустить docker-compose:

```
docker-compose up
```

Документация и примеры запросов доступны по адресу:

```
http://localhost/api/docs/redoc.html
```
