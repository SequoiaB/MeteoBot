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
import MetodiTg
import DecodeQuery
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
    tempInfo = {'city': "?",
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
            InlineKeyboardButton("Domani",callback_data=str(TWO)),
        ],
        [
            InlineKeyboardButton("Custom", callback_data=str(NINE)),
            #InlineKeyboardButton("B4",callback_data=str(FOUR)),
        ],
        [
            InlineKeyboardButton("Esci", callback_data=str(TEN)),
            # InlineKeyboardButton("6", callback_data=str(SIX)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send message with text and appended InlineKeyboard
    await update.message.reply_text("Ciao! per che giornata/e vuoi vedere il meteo?🪟", reply_markup=reply_markup)
    # Tell ConversationHandler that we're in state `FIRST` now
    return RANGE1


async def scelta_giorno_inizio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global tempInfo
    query = update.callback_query
    await query.answer()

    # non serve il dato in teoria
    # dato = int(query.data)
    # print("query.data = ", dato)

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
    global tempInfo
    query = update.callback_query
    await query.answer()
    inizio = int(query.data)
    tempInfo = DecodeQuery.decode_giorno_inizio(inizio, tempInfo)
    keyboard = [
        [
            InlineKeyboardButton("Solo quel giorno", callback_data=str(ONE)),
        ],
        [
            InlineKeyboardButton("2 giorni", callback_data=str(TWO)),
            InlineKeyboardButton("3 giorni", callback_data=str(THREE)),
        ],
        [
            InlineKeyboardButton("4 giorni", callback_data=str(FOUR)),
            InlineKeyboardButton("5 giorni", callback_data=str(FIVE)),
        ],
        [
            InlineKeyboardButton("Esci", callback_data=str(TEN)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="Bene, ora scegli quanti giorni di meteo vuoi vedere dalla data scelta, \n\n_ricorda che sono disponibili i dati fino a 5 giorni da adesso_", reply_markup=reply_markup
    )
    return RANGE3

async def save_fine(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    global tempInfo
    query = update.callback_query
    await query.answer()
    fine = int(query.data)
    tempInfo = DecodeQuery.decode_giorno_fine(fine, tempInfo)
    text = "Che citta' ti interessa?"
    esc_text = MetodiTg.escape_special_chars(text)

    await query.edit_message_text(esc_text, parse_mode="MarkdownV2")
    return RANGE4

async def scelta_city(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    global tempInfo
    city = update.message.text
    tempInfo['city'] = city
    try:
        text = MetodiBot.get_weather_data(tempInfo['city'], tempInfo["start"], tempInfo["finish"])
    except:
        text = "Qualcosa e' andato storto, se vuoi puoi dirlo a @eddichan"
    esc_text = MetodiTg.escape_special_chars(text)

    await update.message.reply_text(esc_text, parse_mode="MarkdownV2")
    await end(update=update, context=context)
    return ConversationHandler.END

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Send a message when the command /help is issued."""
    help_message = '''
'''
    await update.message.reply_text(help_message, parse_mode="MarkdownV2")

async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    
    return ConversationHandler.END

async def end_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    text = "Ci vediamo alla prossima! 👋"
    esc_text = MetodiTg.escape_special_chars(text)
    await query.edit_message_text(esc_text, parse_mode="MarkdownV2")
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
        entry_points=[CommandHandler(["meteo", "start"], enter_cycle)],
        states={
            RANGE1: [
                CallbackQueryHandler(
                    scelta_giorno_fine, pattern="^" + str(ONE) + "$"),
                CallbackQueryHandler(scelta_giorno_fine, pattern="^" + str(TWO) + "$"),
                CallbackQueryHandler(scelta_giorno_inizio, pattern="^" + str(NINE) + "$"),
                CallbackQueryHandler(end_query, pattern="^" + str(TEN) + "$"),
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
                    end_query, pattern="^" + str(TEN) + "$"),
            ],
            RANGE3: [
                CallbackQueryHandler(
                    save_fine, pattern="^" + str(ONE) + "$"),
                CallbackQueryHandler(
                    save_fine, pattern="^" + str(TWO) + "$"),
                CallbackQueryHandler(
                    save_fine, pattern="^" + str(THREE) + "$"),
                CallbackQueryHandler(
                    save_fine, pattern="^" + str(FOUR) + "$"),
                CallbackQueryHandler(
                    save_fine, pattern="^" + str(FIVE) + "$"),
                CallbackQueryHandler(end_query, pattern="^" + str(TEN) + "$"),
            ],
            RANGE4: [
                MessageHandler(filters.TEXT, scelta_city)
            ],
        },
        fallbacks=[CommandHandler("start", enter_cycle)],
    )

    # Add ConversationHandler to application that will be used for handling updates
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("help", help_command))
    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
