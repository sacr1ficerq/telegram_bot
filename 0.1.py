from telegram import (
    Update,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

import telegramcalendar
import messages
import utils

from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler
)


# Enable logging
import logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

from trip import Trip

trip = Trip()
TYPE, CITY, TIME, CONTACTS = range(4)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """asking about types"""
    reply_keyboard = [["Знакомство с городом", "Уличная романтика", "Прикоснуться к прекрасному", "Наедине с природой"]]

    type1 = "Знакомство с городом - " \
            "Если вы хотите погрузиться в " \
            "атмосферу города и насладиться его " \
            "видами, то программа \"знакомство с городом\"."

    type2 = "Уличная романтика - Вы заядлый романтик и " \
            "любитель прекрасного? Тогда вам будет интересно " \
            "исследовать тайные уголки города в поисках аутентичных " \
            "мест. Не забудьте заглянуть на местные барахолки!"

    type3 = "Прикоснуться к прекрасному -Вы творческий человек и " \
            "хотите насладиться жемчужинами города через местную " \
            "архитектуру и живопись, тогда вам сюда!"

    type4 = "Наедине с природой - Вы устали от " \
            "шумного города и хотите побыть в тишине? " \
            "Эта программа поможет вам отдохнуть и " \
            "насладиться очарованием местных пейзажей."

    await update.message.reply_text("Привет. У нас есть всякие туры и мы сейчас про них расскажем."
                                    "Короче у нас есть есть всякие типы поездок вот такие: ")
    await update.message.reply_photo("cats/cat-1.jpg", caption=type1)
    await update.message.reply_photo("cats/cat-2.jpg", caption=type2)
    await update.message.reply_photo("cats/cat-3.jpg", caption=type3)
    await update.message.reply_photo("cats/cat-4.jpg", caption=type4)
    await update.message.reply_text(
        "Выбери себе какой-нить",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Выбери тип"
        ),
    )

    return TYPE

async def type_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """asking about cities."""
    reply_keyboard = [["Новгород"]]

    user = update.message.from_user
    logger.info("Пацанчик %s выбрал %s", user.first_name, update.message.text)
    trip.user = user.username
    trip.type = update.message.text

    await update.message.reply_text(
        "Теперь выбирай город\n"
        "У нас есть на выбор вот такие города:\n"
        "Новгород",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Выбери город"
        ),
    )

    return CITY

async def city_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """asking about time"""

    user = update.message.from_user
    logger.info("Пацанчик %s хочет посетить %s", user.first_name, update.message.text)
    trip.city = update.message.text

    await update.message.reply_text(
        "теперь выбери дату",
        reply_markup=telegramcalendar.create_calendar(),
    )
    print(update.message.text)
    return TIME

async def time_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the info about the user and ends the conversation."""
    await context.bot.send_message(chat_id=update.callback_query.from_user.id, text="Вот тебе контакты: 8 800 555 35 35 \n\n")
    await context.bot.send_message(chat_id=update.callback_query.from_user.id, text="Пока")

    print(trip)

    return ConversationHandler.END

async def inline_handler(update, context):
    query = update.callback_query
    (kind, _, _, _, _) = utils.separate_callback_data(query.data)
    if kind == messages.CALENDAR_CALLBACK:
        await inline_calendar_handler(update, context)

    await time_input(update, context)

async def inline_calendar_handler(update, context):
    selected, date = telegramcalendar.process_calendar_selection(update, context)
    if selected:
        await context.bot.send_message(chat_id=update.callback_query.from_user.id,
                                 text=f"Вы выбрали {date.strftime('%d/%m/%Y')}",
                                 reply_markup=ReplyKeyboardRemove())
        trip.date = date.strftime('%d/%m/%Y')

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "ты че меня отменил.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END



def main():
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("5655793319:AAFUhdmB2e1_gsYLJ28o1ZsK_D0sZFh7uaU").build()

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            TYPE: [MessageHandler(filters.Regex("^(Знакомство с городом|Уличная романтика|Прикоснуться к прекрасному|Наедине с природой)$"), type_input)],
            CITY: [MessageHandler(filters.Regex("^(Новгород)$"), city_input)],
            TIME: [CallbackQueryHandler(inline_handler)]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(conv_handler)
    # Run the bot until the user presses Ctrl-C
    application.run_polling()

if __name__ == "__main__":
    main()