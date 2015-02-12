#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
Adventure
"""
import sys
import argparse
import textwrap
import director


def main():
    """
    Main
    """
    parser = argparse.ArgumentParser(
        prog='Adventure',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
                %(prog)s is a game.
                '''))
    parser.add_argument('-c', '--cheat', action='store_true',
                        dest='cheat',
                        help='show a walkthrough of the game')
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s 1.0')
    args = parser.parse_args()

    if args.cheat:
        print('Walkthrough: take axe, move east, use axe door, move east, move east, move south, move east, bash chest,'
              'take hammer, move west, move north, move west, move west, move west, move south, interact man, e'
              ', use axe tree move south move east, move north, search, take pot, move south, move south, move east, '
              'move north, move east, move south, move east, move north, use ruby altar, use hammer ruby, use pot ashes'
              ', move south, move west, move north, move west, move south, move west, move north, move west, move north'
              ', interact man, y.')
        return

    director.play()
    return


if __name__ == '__main__':
    # Call main() in a manner that will (supposedly) exit gracefully in an interactive prompt
    sys.exit(main())
