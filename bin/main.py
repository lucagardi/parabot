#!/usr/bin/env python3
import json
import logging
import argparse
import configparser
from telegram.ext import Updater

class Parabot(object):
    CONFIG_PATH = '../etc/parabot.conf'
    def init_config(self):
        self.logger.debug('Reading config')
        config = configparser.ConfigParser()
        config.read(self.CONFIG_PATH)

        self.config = config

    def init_logging(self, debug):
        # Init logging
        log          = logging.getLogger(__name__)
        telegram_log = logging.getLogger('telegram')

        # Add console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG if args.debug else logging.INFO)

        # Add formatters and set log levels
        console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)

        log.addHandler(console_handler)
        telegram_log.addHandler(console_handler)

        log.setLevel(logging.DEBUG if args.debug else logging.INFO)
        telegram_log.setLevel(logging.DEBUG if args.debug else logging.INFO)

        self.logger = log

    def init_handlers(self):
        pass

    def __init__(self, debug=False):
        self.init_logging(debug=debug)
        self.init_config()

        # Initializing bot
        self.updater = Updater(token=self.config.get('telegram', 'token'))

        # Init handlers
        self.dispatcher = self.init_handlers()

        # Start the Bot
        self.updater.start_polling()

        # Run the bot until the you presses Ctrl-C or the process receives
        # SIGINT, SIGTERM or SIGABRT. This should be used most of the time,
        # since start_polling() is non-blocking and will stop the bot
        # gracefully.
        self.updater.idle()


if __name__ == '__main__':
    # Handle CLI
    cli_args = argparse.ArgumentParser('Paragliding rides/carsharing integration')
    cli_args.add_argument('-d', '--debug', action='store_true', help='Show debug information')
    args = cli_args.parse_args()

    # Start bot
    Parabot(debug=args.debug)
