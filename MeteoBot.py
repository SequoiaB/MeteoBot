#!/usr/bin/env python
# pylint: disable=unused-argument, import-error
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to keep track of your study and study better
"""
import matplotlib.pyplot as plt
import numpy as np
import time
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, ConversationHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler
import MetodiBot
import MetodiBot2
import MetodiTg
from dotenv import load_dotenv
import os
from io import BytesIO


load_dotenv()
bot_token = os.getenv("BOT_TOKEN")
# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

global tempInfo

# Stages
RANGE1, RANGE2, RANGE3, RANGE4, RANGE5 = range(5)
# Callback data
ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE, TEN, ELEVEN, TWELVE = range(
    12)



async def enter_cycle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global tempInfo
    tempInfo = {'City': "?",
                'start': 0,
                'finish': 0,
                }
    # Build InlineKeyboard where each button has a displayed text
    # and a string as callback_data
    # The keyboard is a list of button rows, where each row is in turn
    # a list (hence `[[...]]`).
    keyboard = [
        [
            InlineKeyboardButton("Oggi", callback_data=str(ONE)),
            InlineKeyboardButton("Domani",
                                 callback_data=str(TWO)),
        ],
        [
            InlineKeyboardButton(
                "Custom", callback_data=str(THREE)),
            #InlineKeyboardButton("B4",callback_data=str(FOUR)),
        ],
        [
            InlineKeyboardButton("Esci", callback_data=str(TEN)),
            # InlineKeyboardButton("6", callback_data=str(SIX)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send message with text and appended InlineKeyboard
    await update.message.reply_text("Ciao, che materia vuoi studiare?", reply_markup=reply_markup)
    # Tell ConversationHandler that we're in state `FIRST` now
    return RANGE1


async def scelta_giorno_inizio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    await query.answer()
    # print(query.data)
    dato = int(query.data)

    keyboard = [
        [
            InlineKeyboardButton("Oggi", callback_data=str(ONE)),
        ],
        [
            InlineKeyboardButton("Domani", callback_data=str(TWO)),
            InlineKeyboardButton("Dopo domani", callback_data=str(THREE)),
        ],
        [
            InlineKeyboardButton("Tra 3 giorni", callback_data=str(FOUR)),
            InlineKeyboardButton("Tra 4 giorni", callback_data=str(FIVE)),
        ],
        [

            InlineKeyboardButton("Esci", callback_data=str(TEN)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="A partire da che giorno vuoi vedere il meteo?", reply_markup=reply_markup
    )
    return RANGE2

async def scelta_giorno_fine(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    await query.answer()
    # print(query.data)
    inizio = int(query.data)
    print(inizio)
    keyboard = [
        [
            InlineKeyboardButton("1", callback_data=str(ONE)),
        ],
        [
            InlineKeyboardButton("2", callback_data=str(TWO)),
            InlineKeyboardButton("3", callback_data=str(THREE)),
        ],
        [
            InlineKeyboardButton("4", callback_data=str(FOUR)),
            InlineKeyboardButton("5", callback_data=str(FIVE)),
        ],
        [
            InlineKeyboardButton("Esci", callback_data=str(TEN)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="Bene, ora scegli quanto tempo far durare le tue sessioni di studio", reply_markup=reply_markup
    )
    return RANGE3

async def scelta_city(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    global tempInfo
    query = update.callback_query
    await query.answer()
    # print(query.data)
    dato = int(query.data)
    if dato == 0:
        tempInfo['start'] = 0
        tempInfo['finish'] = 1
        tempInfo["City"] = "Padova"
        text = MetodiBot.get_weather_data(tempInfo['City'], tempInfo["start"], tempInfo["finish"])
        esc_text = MetodiTg.escape_special_chars(text)
    await query.edit_message_text(esc_text, parse_mode="MarkdownV2")
    return RANGE4

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Send a message when the command /help is issued."""
    help_message = '''
'''
    await update.message.reply_text(help_message, parse_mode="MarkdownV2")


async def stampa(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    photo = ""
    await update.message.reply_photo(photo, caption="aa", parse_mode="MarkdownV2")

async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over.
    """
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Scrivimi quando vuoi vedere il meteo 👋")
    return ConversationHandler.END

def main() -> int:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(bot_token).build()

    # Setup conversation handler with the states FIRST and SECOND
    # Use the pattern parameter to pass CallbackQueries with specific
    # data pattern to the corresponding handlers.
    # ^ means "start of line/string"
    # $ means "end of line/string"
    # So ^ABC$ will only allow 'ABC'
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("focus", enter_cycle)],
        states={
            RANGE1: [
                CallbackQueryHandler(
                    scelta_city, pattern="^" + str(ONE) + "$"),
                CallbackQueryHandler(
                    scelta_city, pattern="^" + str(TWO) + "$"),
                CallbackQueryHandler(
                    scelta_city, pattern="^" + str(THREE) + "$"),
                CallbackQueryHandler(
                    scelta_giorno_inizio, pattern="^" + str(FOUR) + "$"),
                CallbackQueryHandler(end, pattern="^" + str(TEN) + "$"),
            ],
            RANGE2: [
                CallbackQueryHandler(
                    scelta_giorno_fine, pattern="^" + str(ONE) + "$"),
                CallbackQueryHandler(
                    scelta_giorno_fine, pattern="^" + str(TWO) + "$"),
                CallbackQueryHandler(
                    scelta_giorno_fine, pattern="^" + str(THREE) + "$"),
                CallbackQueryHandler(
                    scelta_giorno_fine, pattern="^" + str(FOUR) + "$"),
                CallbackQueryHandler(
                    scelta_giorno_fine, pattern="^" + str(FIVE) + "$"),
                CallbackQueryHandler(
                    end, pattern="^" + str(TEN) + "$"),
            ],
            RANGE3: [
                CallbackQueryHandler(
                    scelta_city, pattern="^" + str(ONE) + "$"),
                CallbackQueryHandler(
                    scelta_city, pattern="^" + str(TWO) + "$"),
                CallbackQueryHandler(
                    scelta_city, pattern="^" + str(THREE) + "$"),
                CallbackQueryHandler(
                    scelta_city, pattern="^" + str(FOUR) + "$"),
                CallbackQueryHandler(
                    scelta_city, pattern="^" + str(FIVE) + "$"),
                CallbackQueryHandler(end, pattern="^" + str(TEN) + "$"),
            ],

        },
        fallbacks=[CommandHandler("start", enter_cycle)],
    )

    # Add ConversationHandler to application that will be used for handling updates
    application.add_handler(conv_handler)

    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("print", stampa))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
