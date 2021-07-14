import configparser
import json
from datetime import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CommandHandler, ConversationHandler, CallbackQueryHandler
from telegram.ext.callbackcontext import CallbackContext
from telegram.constants import PARSEMODE_HTML
import requests


def ParaglidableHandler(bot):
    """ Telegram bot-aware ConversationHandler that shows data from Paraglidable APIs. """
    # Define steps
    SHOW_SITES = 1

    # Retrieve JSON data from Paraglidable
    url = '%s%s' % (
        bot.config.get('paraglidable', 'url'),
        bot.config.get('paraglidable', 'token'))
    data = requests.get(url).json()

    def show_sites(update, context):
        """ Second step of the handler, show a reply containing formatted sites. """

        # Get CallbackQuery from Update
        query = update.callback_query

        # CallbackQueries need to be answered, even if no notification to the user is 
        # needed . Some clients may have trouble otherwise. 
        # See https://core.telegram.org/bots/api#callbackquery
        query.answer()

        # Cook a nicely looking HTML-formatted answer with the sites and percentages
        day_str = datetime.strptime(query.data, "%Y-%m-%d").strftime("%a %b %d")
        reply = "Here's the Paraglidable score for the %s:\n" % day_str
        for site in data[query.data]:
            reply += '<b>{}</b>: {:.0%} flyable {:.0%} XC\n'.format(
                site['name'],
                float(site['forecast']['fly']),
                float(site['forecast']['XC']))

        # Answer by editing the message
        query.edit_message_text(text=reply, parse_mode=PARSEMODE_HTML)



    def start(update, context):
        """ Show a list of dates to pick from using an InlineKeyboardButton object. """
        # Cook keyboard, three rows
        keyboard = [[], [], [], []]
        slot = 0

        # Fill keyboard slots with dates and their callback data
        for day, site in data.items():
            if not site:
                continue

            # Properly format the data for visualization, retain raw data for callback
            day_str = datetime.strptime(day, "%Y-%m-%d").strftime("%a %b %d")
            keyboard[slot//3].append(InlineKeyboardButton(day_str, callback_data=day))
            slot = slot + 1

        # Send the reply
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(text="Select a day:", reply_markup=reply_markup)

        # Go to next state, ready to show the sites
        return SHOW_SITES

    # Instanciate a bot-aware ConversationHandler and return it
    paraglidable_handler = ConversationHandler(
        entry_points=[CommandHandler('paraglidable', start)],
        states={SHOW_SITES: [CallbackQueryHandler(show_sites)]},
        fallbacks=[CommandHandler('paraglidable', start)]
    )

    return paraglidable_handler
