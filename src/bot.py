import configparser
from datetime import datetime
import json
import logging

import dataset
import pytz

from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from handlers.paraglidable import ParaglidableHandler

class Bot(object):
    CONFIG_PATH = '../etc/parabot.conf'
    DB_PATH = '../var/parabot.db'

    @classmethod
    def get_config(cls):
        return 

    def say_hello(self, instance, update):
        print(instance)
        print(update)


    def action_router(self, update, context):
        """
        Main action router, handler for Telegram messages.
        Should be used to provide the correct actions decisions
        and trigger a reply
        :param update: Update to be handled
        :param context: CallbackContext
        :return: None
        """

        # Avoids flooding chats with replies for old messages
        if update.message.date < self.starttime:
            self.logger.debug('Message from the past! %s < %s' % (update.message.date, self.starttime) )
            return

        pass

        # Handle actions in here
        # self.logger.debug('Action not routed: %s' % update)
        # update.message.reply_text("unrouted action")


    # def error_router(self, update, context):
    #     """
    #     Main telegram error handling
    #     :param update: update that caused the error
    #     :param error: telegram error to be reported
    #     :return:
    #     """
    #     self.logger.error('Update "%s" caused error "%s"', update, context)

    def init_config(self):
        config = configparser.ConfigParser()
        config.read(self.CONFIG_PATH)
        self.config = config


    def init_logging(self, debug):
        # Init logging
        log          = logging.getLogger(__name__)
        telegram_log = logging.getLogger('telegram')

        # Add console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG if debug else logging.INFO)

        # Add formatters and set log levels
        console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)

        log.addHandler(console_handler)
        telegram_log.addHandler(console_handler)

        log.setLevel(logging.DEBUG if debug else logging.INFO)
        telegram_log.setLevel(logging.DEBUG if debug else logging.INFO)

        self.logger = log


    def init_admins(self):
        # Verify if an administrator exists
        admins = list(self.db['administrators'].find())
        if not admins:
            self.logger.info('No admin found, identify using key %s' % 
            self.config.get('bot', 'admin_key'))

            return

        self.logger.debug('Admins: %s' % admins)


    def init_handlers(self):
        # Retrieve Dispatcher from the Updater
        dispatcher = self.updater.dispatcher

        # Handle text messages with a MessageHandler
        # message_handler = MessageHandler(Filters.text, self.action_router)
        # dispatcher.add_handler(message_handler)

        # Handle errors with an ErrorHandler
        # dispatcher.add_error_handler(self.error_router)

        # Handle commands with CommandHandlers
        print(ParaglidableHandler(self))
        dispatcher.add_handler(ParaglidableHandler(self))

        self.dispatcher = dispatcher


    def init_database(self):
        db = dataset.connect('sqlite:///%s' % self.DB_PATH)

        self.db = db


    def __init__(self, debug=False):
        self.init_logging(debug=debug)
        self.init_config()
        self.init_database()

        # Save a offset-aware timestamp to compare in the future
        self.tz = pytz.timezone(self.config.get('bot', 'timezone'))
        self.starttime = self.tz.localize(datetime.now())

        # Initializing bot
        self.updater = Updater(token=self.config.get('telegram', 'token'))
        
        # Init handlers
        self.init_handlers()

        # Verify administration rights
        self.init_admins()

        # Start the Bot
        self.updater.start_polling()

        # Run the bot until the you presses Ctrl-C or the process receives
        # SIGINT, SIGTERM or SIGABRT. This should be used most of the time,
        # since start_polling() is non-blocking and will stop the bot
        # gracefully.
        self.updater.idle()
