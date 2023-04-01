![example workflow](https://github.com/ifyoumasha/foodgram-project-react/actions/workflows/main.yml/badge.svg)

### Адрес проекта:

http://foodgram-recipes.sytes.net/

#логин от админки: maria
#пароль: foodgram123

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
http://api/docs/redoc.html
```

### Как запустить проект на удалённом сервере:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:ifyoumasha/foodgram-project-react.git
```

```
cd foodgram-project-react
```

Скопировать файлы docker-compose.yml и nginx.conf из папки infra на удалённый сервер:

```
cd foodgram-project-react/infra/
```

```
scp docker-compose.yml <username>@<IP>:/home/<username>/ # username - имя пользователя на сервере
scp nginx.conf <username>@<IP>:/home/<username>/         # IP - публичный IP сервера
```

В настройках репозитория на GitHub создать переменные окружения в разделе Settings -> Secrets -> Actions:

```
SSH_KEY # приватный ssh-ключ
PASSPHRASE # пароль от ssh-ключа
DOCKER_USERNAME # логин от DockerHub
DOCKER_PASSWORD # пароль от DockerHub
SECRET_KEY # секретный ключ от Django-проекта
HOST # публичный IP сервера
USER # имя пользователя на сервере
TELEGRAM_TO # ID от аккаунта в телеграмк для отправки сообщения о успешном деплое
TELEGRAM_TOKEN # токен от телеграм-бота, в который придёт сообщение о успешном деплое

DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД
```

Запускаем docker-compose на сервере:

```
sudo docker-compose up -d
```

Теперь в контейнере нужно создать и выполнить миграции, собрать статику и создать суперпользователя. Выполняем по очереди команды:

```
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic --no-input
docker-compose exec web python manage.py createsuperuser
```

### Как заполнить базу данных ингредиентами:

Скопировать файл ingredients.json из папки data на удалённый сервер:

```
cd foodgram-project-react/data/
```

```
scp ingredients.json <username>@<IP>:/home/<username>/ 
# username - имя пользователя на сервере
# IP - публичный IP сервера
```

Скопировать файл ingredients.json на удалённый сервер:

```
sudo docker cp ingredients.json <CONTAINER ID>:/app/
sudo docker-compose exec backend python manage.py loaddata ingredients.json
```

### Автор проекта:
Кляхина Мария
