import requests
from requests import ConnectionError
from requests import ReadTimeout
from requests import HTTPError
from dotenv import load_dotenv
from os import getenv
import os
import telegram
from telegram.error import NetworkError
import time
import logging
from logging.handlers import RotatingFileHandler


def set_logger():
    # It means DEBUG level - https://docs.python.org/3.6/library/logging.html#levels
    log_level = 10
    logger = logging.getLogger("devman_bot_logger")
    max_file_size = 1024 * 1024 * 10
    log_path = os.path.join(bot_home, 'bot.log')
    if not len(logger.handlers):
        logger.setLevel(log_level)
        formatter = logging.Formatter('%(asctime)s - %(filename)s --> %(funcName)s - %(levelname)s - %(message)s')
        handler = RotatingFileHandler(log_path, maxBytes=max_file_size, backupCount=3, encoding='utf-8')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger


def run_bot(
        devman_token=None,
        chat_id=None,
        bad_message=None,
        good_message=None
):
    api_url = 'https://dvmn.org/api/long_polling'
    devman_url = 'https://dvmn.org/'
    headers = {'Authorization': 'Token {}'.format(devman_token)}
    params = {'timestamp': ''}
    logger.info("Бот запущен!")
    while True:
        try:
            response = requests.get(api_url, headers=headers, params=params)
            response.raise_for_status()
            json_data = response.json()
            if json_data['status'] == 'found':
                for attempt in json_data['new_attempts']:
                    if attempt['is_negative']:
                        message = bad_message.format(
                            attempt['lesson_title'],
                            attempt['lesson_url']
                        )
                    else:
                        message = good_message.format(
                            attempt['lesson_title'],
                            devman_url
                        )
                    logger.info(message)
                    bot.send_message(chat_id=chat_id, text=message)
                params['timestamp'] = json_data['last_attempt_timestamp']
            if json_data['status'] == 'timeout':
                params['timestamp'] = json_data['timestamp_to_request']
        except (ConnectionError, ReadTimeout, HTTPError) as error:
            logger.error("Возникла ошибка при обращении к {}:\n{}".format(
                api_url,
                error
            ))
            time.sleep(5)
        except NetworkError as error:
            logger.error('Возникла ошибка при обращении к Telegram :\n{}'.format(
                error
            ))
            time.sleep(5)


if __name__ == '__main__':
    load_dotenv()
    devman_token = getenv('DEVMAN_TOKEN')
    bot_home = getenv('BOT_HOME')
    chat_id = getenv('TELEGRAM_CHANNEL_NAME')
    bot_token = getenv('TELEGRAM_BOT_TOKEN')
    bad_message = 'У вас проверили работу "{}"\n' \
                  'К сожалению, в работе нашлись ошибки.\n' \
                  'Подробности: https://dvmn.org{}'
    good_message = 'У вас проверили работу "{}"\n' \
                   'Преподавателю все понравилось, ' \
                   'можно приступать к следующему уроку: {}modules!'

    bot = telegram.Bot(token=bot_token)

    logger = set_logger()
    run_bot(
        devman_token=devman_token,
        chat_id=chat_id,
        bad_message=bad_message,
        good_message=good_message
    )
