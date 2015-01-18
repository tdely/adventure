#!/usr/bin/env python3
# -*- encoding: utf-8 -*-§
import player
import world
import items
import sys
"""
Mediates commands and changes
"""

DEBUG = True

world.initialize_world()
actor = player.Player(world.start_area)
actor.inventory.append(items.trinket_list['axe'])


def menu():
    pass


def control():
    """
    Method for player interaction
    """
    rcode = None
    string = input(': ').lower()
    arguments = string.split()
    command = arguments.pop(0)

    options = {'help': show_help,
               'use': use,
               'interact': interact,
               'inventory': inventory,
               'move': move,
               'exit': exit_game, }
    try:
        rcode = options[command](*arguments)
    except KeyError as e:
        print("I don't know what '{0}' is..".format(command))
        print("Debug: KeyError {0}".format(e)) if DEBUG else None
    except TypeError as e:
        print("Too much information.")
        print("Debug: TypeError {0}".format(e)) if DEBUG else None
    if rcode is 'exit':
        return False
    return True


def show_help():
    print('use [item] [target],  interact [object],  inventory,  move [direction],  bash [object]')


def use(this=None, that=None):
    if this is None and that is None:
        print("You can't use nothing.")
        return False
    elif that is None:
        print("You must use '{0}' on something.".format(this))
    print('Use is not implemented')


def interact(obj=None):
    if obj is None:
        print("You can't interact with nothing.")
        return False
    print('Interact is not implemented')


def inventory():
    """
    List player inventory
    """
    if len(actor.inventory) > 0:
        print('Inventory:')
        for i in actor.inventory:
            print(i.name)
    else:
        print('Your inventory is empty.')


def move(direction=None):
    """
    Move the player
    """
    if direction is None:
        print("You can't move without a direction.")
        return False
    if direction not in ('north', 'west', 'south', 'east'):
        print("Unknown direction '{0}'.".format(direction))
        return False
    if actor.move(direction):
        print('Moved {0}.'.format(direction))
        enter_area()
        return True
    print("You can't move {0}.".format(direction))
    return False


def bash():
    print('Bash is not implemented')


def enter_area():
    y, x = actor.get_position()
    world.world_map[y][x].describe()


def exit_game():
    """
    placeholder
    """
    confirm = input('Are you sure you want to exit the game? (y/n) ').lower()
    if confirm in ('y', 'yes'):
        return 'exit'
    else:
        print('Continuing game.')
        return False


def play():
    """
    placeholder
    """
    enter_area()
    while control():
        pass

    # Testing
    # print(world.world_map[1][0])
    # print(world.world_map[1][0].exit_available('north'))
    # print(world.world_map[1][0].unblock_exit('north'))
    # print(world.world_map[1][0].unblock_exit('south'))
    # print(world.world_map[1][0])
    #
    # p1 = player.Player((0, 0))
    # p1.inventory.append(items.itemlist['axe'])
    # p1.get_inventory()
    # p1.inventory.remove(items.itemlist['axe'])
    # p1.get_inventory()
    #
    # print(items.Furniture('rock', 'a large rock', False, False))
    # print(items.itemlist['ruby'])
    #
    # world.world_map[1][0].describe()