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
        print('Take the axe and move east. Use the axe on the door, move east three times, bash the barrel and retrieve'
              ' the key. Interact with the game and win three times, then take the medallion. Move west, then south, '
              'then east again. Bash the chest and take the hammer. Move out of the cave and back to the first area, '
              "then go south and interact with the man, Give the answer 'e' to his riddle. Use the axe on the tree, "
              'then move south, east, and back north. Search the area, and take the pot that is found. Now go south, '
              'south, east, north, east, south, east, north. Use the ruby with the altar, then use the hammer on the '
              'ruby. Use the pot with the ashes and go back and interact with the man.\n\n A save at the very end of'
              "the game is available through 'load finalsave.json'")
        return

    director.play()
    return


if __name__ == '__main__':
    # Call main() in a manner that will (supposedly) exit gracefully in an interactive prompt
    sys.exit(main())
