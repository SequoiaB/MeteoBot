import matplotlib.pyplot as plt
import numpy as np
import time
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, ConversationHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler
import MetodiBot

async def today_weather(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    message = '''
'''
    await update.message.reply_text(message, parse_mode="MarkdownV2")