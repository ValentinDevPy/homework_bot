import logging
import os
import sys
import time
from http import HTTPStatus
from logging import StreamHandler

import requests
import telegram
from dotenv import load_dotenv

from exceptions import MessageSentError, ResponseError, HomeworksIsNotListError, NoRequiredTokens

load_dotenv()

PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_TIME = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}

HOMEWORK_STATUSES = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = StreamHandler(stream=sys.stdout)
handler.setFormatter(formatter)
logger.addHandler(handler)


def send_message(bot: telegram.Bot, message: str):
    """Функция отправки новых сообшений в Telegram."""
    try:
        bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=message,
        )
        logger.info(f'Сообщение отправлено: {message}')
    except MessageSentError:
        logger.error('Ошибка при отправке сообщения')


def get_api_answer(current_timestamp: int):
    """Логика работы с внешним API Яндекс.Домашки."""
    timestamp = current_timestamp or int(time.time())
    params = {'from_date': timestamp}
    try:
        response = requests.get(ENDPOINT, headers=HEADERS, params=params)
        if response.status_code != HTTPStatus.OK:
            error_message = 'Эндпоинт API Яндекс.Домашка недоступен'
            logger.error(error_message)
            raise ResponseError(error_message)
        return response.json()
    except Exception as error:
        logger.error(f'Ошибка при запросе {error}')
        raise ResponseError('Ошибка при запросе к API Яндекс.Домашка')


def check_response(response):
    """Провека ответа внешнего API на соответсвие необходимому формату."""
    if isinstance(response, list):
        response = response[0]
    if not isinstance(response.get('homeworks'), list):
        logger.error('Домашние работы пришли не в виде списка')
        raise HomeworksIsNotListError(
            'Домашние работы пришли не в виде списка'
        )
    return response.get('homeworks')


def parse_status(homework):
    """Получение из ответа API необходимых данных."""
    name_error_message = 'Нет имени домашней работы'
    status_error_message = 'Пришёл некорректный статус проверки'
    
    if homework:
        if isinstance(homework, dict):
            last_homework = homework
        else:
            last_homework = homework[0]
        homework_name = last_homework.get('homework_name')
        if not homework_name:
            logger.error(name_error_message)
            raise KeyError(name_error_message)
        homework_status = last_homework.get('status')
        verdict = HOMEWORK_STATUSES.get(homework_status)
        if not verdict:
            logger.error(status_error_message)
            raise KeyError(status_error_message)
        return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def check_tokens():
    """Проверка всех необходимых переменных токенов для работы бота."""
    if PRACTICUM_TOKEN and TELEGRAM_TOKEN and TELEGRAM_CHAT_ID:
        return True
    return False


def main():
    """Основная логика работы бота."""
    current_status = None
    if not check_tokens():
        tokens_error_message = 'Отсутствует один или несколько токенов'
        logger.critical(tokens_error_message)
        raise NoRequiredTokens(tokens_error_message)
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time())
    while True:
        try:
            response = get_api_answer(current_timestamp)
            homeworks = check_response(response)
            message = parse_status(homeworks)
            current_timestamp = int(time.time())
            if message != current_status:
                current_status = message
                send_message(bot, message)
            else:
                logger.debug('Новых данных нет')
        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            if message != current_status:
                send_message(bot, message)
        time.sleep(RETRY_TIME)


if __name__ == '__main__':
    main()
