#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
import sys
import argparse
import textwrap
import world


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
                        version='%(prog)s 0.5')
    args = parser.parse_args()

    if args.cheat:
        # TODO: write a 'walkthrough' after game is finished
        print('Walkthrough.')
        return

    world.initialize_world()

    # Testing
    print(world.worldmap[1][0])
    print(world.worldmap[1][0].exit_available('north'))
    print(world.worldmap[1][0].unblock_exit('north'))
    print(world.worldmap[1][0].unblock_exit('south'))
    print(world.worldmap[1][0])
    return


if __name__ == '__main__':
    sys.exit(main())