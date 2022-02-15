import os
from logging import Handler
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
from dotenv import load_dotenv
from detect_intent import detect_intent_text

load_dotenv()


def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(bot, update):
    """Echo the user message."""
    chat_id = update.message.chat_id
    text = update.message.text
    intent = detect_intent_text(
        project_id=project_id,
        session_id=chat_id,
        text=text,
        language_code='ru'
    )
    bot.send_message(chat_id=chat_id,
                     text=intent.query_result.fulfillment_text)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(os.environ['TELEGRAM_TOKEN'])

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)
project_id = os.environ['PROJECT_ID']
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = \
    "/home/alex/Downloads/deep-mechanism-340911-b0e1d45bfedc.json"

if __name__ == '__main__':
    main()
