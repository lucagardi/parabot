#!/usr/bin/env python3
import argparse
import sys

# Dirty trick until packaged
sys.path.insert(1, '../src')
from bot import Bot

if __name__ == '__main__':
    # Handle CLI arguments
    cli_args = argparse.ArgumentParser('Paragliding rides/carsharing integration')
    cli_args.add_argument('-d', '--debug', action='store_true', help='Show debug information')
    args = cli_args.parse_args()

    # Start bot, resistence is futile
    Bot(debug=args.debug)
