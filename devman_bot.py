import requests
from requests import ConnectionError
from requests import ReadTimeout
from dotenv import load_dotenv
from os import environ
from os import getenv
import telegram
from telegram.error import NetworkError


def send_to_telegram(text, chat_id, token):
    # http://spys.one/proxys/US/
    environ['HTTPS_PROXY'] = 'https://70.102.86.204:8080'
    bot = telegram.Bot(token=token)
    bot.send_message(chat_id=chat_id, text=text)


def run_bot():
    while True:
        try:
            response = requests.get(api_url, headers=headers, params=params)
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
        except (ConnectionError, ReadTimeout):
            print('Timeout from Devman!')
        except NetworkError as error:
            print('Error during send to Telegram :\n{}'.format(error))


if __name__ == '__main__':
    load_dotenv()
    api_url = 'https://dvmn.org/api/long_polling'
    devman_token = getenv('DEVMAN_TOKEN')
    devman_url = 'https://dvmn.org/'
    headers = {'Authorization': 'Token {}'.format(devman_token)}
    params = {'timestamp': ''}
    chat_id = getenv('TELEGRAM_CHANNEL_NAME')
    bot_token = getenv('TELEGRAM_BOT_TOKEN')
    bad_message = 'У вас проверили работу "{}"\n' \
                  'К сожалению, в работе нашлись ошибки.\n' \
                  'Подробности: https://dvmn.org/{}'
    good_message = 'У вас проверили работу "{}"\n' \
                   'Преподавателю все понравилось, ' \
                   'можно приступать к следующему уроку: {}modules!'
    run_bot()
