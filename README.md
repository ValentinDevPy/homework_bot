### Homework Bot


## Телеграм-бот для отслеживания статуса проверки домашней работы на Яндекс.Практикум.
Присылает сообщения, когда статус изменен - взято в проверку, есть замечания, зачтено.


### Технологии:
- flake8==3.9.2
- flake8-docstrings==1.6.0
- pytest==6.2.5
- python-dotenv==0.19.0
- python-telegram-bot==13.7
- requests==2.26.0

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/ValentinDevPy/homework_bot.git
```

```
cd homework_bot
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Записать в переменные окружения (файл .env) необходимые ключи:
- токен профиля на Яндекс.Практикуме (PRACTICUM_TOKEN)
- токен телеграм-бота (BOT_TOKEN)
- свой ID в телеграме (TELEGRAM_CHAT_ID)


Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```
