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

STATE1, STATE2 = range(2)
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

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Send a message when the command /help is issued."""
    help_message = '''
'''
    await update.message.reply_text(help_message, parse_mode="MarkdownV2")

async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = "Ok, scrivimi quando ti servono informaizoni sul meteo!☀️🍃"
    try:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(text)
    except:
        await update.message.reply_text(text)

    return ConversationHandler.END

async def scegli_luogo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global tempInfo
    tempInfo = {
                'city': "?",
                'giorno': 0,
                }
    text = "Ciao! che citta ti interessa?"
    await update.message.reply_text(text)
    return STATE1

async def scegli_giorno(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global tempInfo
    city = update.message.text
    tempInfo['city'] = city
    reply_keyboard = MetodiBot.gestioneGiorni()

    keyboard = [
        [
            InlineKeyboardButton(str(reply_keyboard[0][0]), callback_data=str(ONE)),
            InlineKeyboardButton(str(reply_keyboard[1][0]),callback_data=str(TWO)),
        ],
        [
            InlineKeyboardButton(str(reply_keyboard[2][0]), callback_data=str(THREE)),
            InlineKeyboardButton(str(reply_keyboard[3][0]), callback_data=str(FOUR)),
        ],
        [
            InlineKeyboardButton(str(reply_keyboard[4][0]), callback_data=str(FIVE)),
            InlineKeyboardButton(str(reply_keyboard[5][0]), callback_data=str(SIX)),
        ],
        [
            InlineKeyboardButton("Esci", callback_data=str(SEVEN)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send message with text and appended InlineKeyboard
    await update.message.reply_text("Per che giornata vuoi vedere il meteo?🪟", reply_markup=reply_markup)
    # Tell ConversationHandler that we're in state `FIRST` now
    return STATE2

async def meteo_per_giorno_scelto(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    global tempInfo
    query = update.callback_query
    await query.answer()
    data = int(query.data)
    tempInfo['giorno'] = data
    try:
        text = MetodiBot.get_weather_data_single_day(tempInfo["city"], tempInfo['giorno'])
    except: 
        text = """*Qualcosa è andato storto*\. _Probabilmente non sono riuscito a trovare la città\.
Aspetta il prosssimo aggiornameto perché venga risolto il problema\._
*Se vuoi condividi l'errore mandando uno screenshot della chat a @quality365*\."""
    await query.edit_message_text(text, parse_mode="MarkdownV2")
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
    giorno_singolo = ConversationHandler(
        entry_points=[CommandHandler(["meteo", "start"], scegli_luogo)],
        states = {
            STATE1: [MessageHandler(filters.TEXT, scegli_giorno)
                     ],
            STATE2: [CallbackQueryHandler(meteo_per_giorno_scelto , pattern="^" + str(ONE) + "$"),
                     CallbackQueryHandler(meteo_per_giorno_scelto , pattern="^" + str(TWO) + "$"),
                     CallbackQueryHandler(meteo_per_giorno_scelto , pattern="^" + str(THREE) + "$"),
                     CallbackQueryHandler(meteo_per_giorno_scelto , pattern="^" + str(FOUR) + "$"),
                     CallbackQueryHandler(meteo_per_giorno_scelto , pattern="^" + str(FIVE) + "$"),
                     CallbackQueryHandler(meteo_per_giorno_scelto , pattern="^" + str(SIX) + "$"),
                     CallbackQueryHandler(end , pattern="^" + str(SEVEN) + "$"),
                ],
            },
        fallbacks=[CommandHandler(["meteo", "start"], scegli_giorno)],
    )
    
    application.add_handler(giorno_singolo)
    application.add_handler(CommandHandler("help", help_command))
    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()

