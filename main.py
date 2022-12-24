import constants as keys
import responses

from telegram.ext import *


print("Bot started...")


def start_command(update, context):
    update.message.reply_text("start_default")


def help_command(update, context):
    update.message.reply_text("help_default")


def handle_message(update, context):
    text = str(update.message.text).lower()
    response = responses.sample_response(text)

    update.message.reply_text(response)


def main():
    updater = Updater(keys.API_KEY, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", help_command))

    dp.add_handler(MessageHandler(Filters.text, handle_message))

    updater.start_polling(5)
    updater.idle()


main()



