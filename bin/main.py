#!/usr/bin/env python3
import argparse
import sys

sys.path.insert(1, '../src')
from bot import Bot

if __name__ == '__main__':
    # Handle CLI
    cli_args = argparse.ArgumentParser('Paragliding rides/carsharing integration')
    cli_args.add_argument('-d', '--debug', action='store_true', help='Show debug information')
    args = cli_args.parse_args()

    # Start bot
    Bot(debug=args.debug)




