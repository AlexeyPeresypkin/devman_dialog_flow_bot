import logging
import os

import telegram
from dotenv import load_dotenv
import random

import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType

from dialog_flow_bot.detect_intent import detect_intent_text

load_dotenv()


def send_log_info(chat_id, token, text):
    bot = telegram.Bot(token=token)
    bot.send_message(chat_id=chat_id, text=text)


def echo(event, vk_api):
    user_id = event.user_id
    text = event.text
    intent = detect_intent_text(project_id, user_id, text, 'ru')
    if not intent.query_result.intent.is_fallback:
        vk_api.messages.send(
            user_id=event.user_id,
            message=intent.query_result.fulfillment_text,
            random_id=random.randint(1, 1000)
        )


class BotLogsHandler(logging.Handler):
    def __init__(self, telegram_token, chat_id):
        super().__init__()
        self.telegram_token = telegram_token
        self.chat_id = chat_id

    def emit(self, record):
        log_entry = self.format(record)
        send_log_info(
            chat_id=self.chat_id,
            token=self.telegram_token,
            text=log_entry
        )


project_id = os.environ['PROJECT_ID']
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = \
    "/home/alex/Downloads/deep-mechanism-340911-b0e1d45bfedc.json"
'''
path to your key.json, visit 
https://cloud.google.com/docs/authentication/getting-started 
to create a service account
'''

logging.basicConfig(format="%(asctime)s %(process)d %(levelname)s %(message)s")
logger = logging.getLogger('TelegramLoger')
logger.setLevel(logging.DEBUG)
handler = BotLogsHandler(os.environ['LOG_CHAT_ID'], os.environ['CHAT_ID'])
logger.addHandler(handler)

if __name__ == "__main__":
    logger.info('Приложение vk_bot стартовало')
    vk_session = vk.VkApi(token=os.environ['VK_TOKEN'])
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            try:
                echo(event, vk_api)
            except Exception as message:
                logger.debug(message)
