import requests
from requests import ConnectionError
from requests import ReadTimeout
from requests import HTTPError
from dotenv import load_dotenv
from os import environ
from os import getenv
import telegram
from telegram.error import NetworkError
import time


def send_to_telegram(text, chat_id, token):
    # http://spys.one/proxys/US/
    proxy_url = getenv('HTTPS_PROXY')
    environ['HTTPS_PROXY'] = proxy_url
    bot = telegram.Bot(token=token)
    bot.send_message(chat_id=chat_id, text=text)


def run_bot(
        devman_token=None,
        chat_id=None,
        bot_token=None,
        bad_message=None,
        good_message=None
):
    api_url = 'https://dvmn.org/api/long_polling'
    devman_url = 'https://dvmn.org/'
    headers = {'Authorization': 'Token {}'.format(devman_token)}
    params = {'timestamp': ''}
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
                    send_to_telegram(message, chat_id, bot_token)
                params['timestamp'] = json_data['last_attempt_timestamp']
            if json_data['status'] == 'timeout':
                params['timestamp'] = json_data['timestamp_to_request']
        except (ConnectionError, ReadTimeout, HTTPError) as error:
            print(error)
            time.sleep(5)
        except NetworkError as error:
            print('Error during send to Telegram :\n{}'.format(error))
            time.sleep(5)


if __name__ == '__main__':
    load_dotenv()
    devman_token = getenv('DEVMAN_TOKEN')
    chat_id = getenv('TELEGRAM_CHANNEL_NAME')
    bot_token = getenv('TELEGRAM_BOT_TOKEN')
    bad_message = 'У вас проверили работу "{}"\n' \
                  'К сожалению, в работе нашлись ошибки.\n' \
                  'Подробности: https://dvmn.org{}'
    good_message = 'У вас проверили работу "{}"\n' \
                   'Преподавателю все понравилось, ' \
                   'можно приступать к следующему уроку: {}modules!'
    run_bot(
        devman_token=devman_token,
        chat_id=chat_id,
        bot_token=bot_token,
        bad_message=bad_message,
        good_message=good_message
    )
