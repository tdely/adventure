#!/usr/bin/env python3
# -*- encoding: utf-8 -*-§
import player
import world
import items
"""
Mediates commands and changes
"""

world.initialize_world()


def menu():
    pass


def control():
    """
    Method for player interaction
    """
    string = input(':')
    arguments = string.split()
    command = arguments.pop(0)

    options = {'help': show_help,
               'use': use,
               'interact': interact,
               'inventory': inventory,
               'move': move, }
    try:
        if len(arguments) is 0:
            options[command]()
        else:
            options[command](arguments)
    except KeyError:
        print("I don't know what '{0}' is..".format(command))
        pass
    except TypeError as e:
        if 'missing' in e.__str__() and len(arguments) > 0:
            print("{0} '{1}' on what?".format(command, ' '.join(arguments)))
        elif 'missing' in e.__str__():
            print("'{0}' requires more information.".format(command))
        elif 'takes' in e.__str__():
            print("Too many subjects for '{0}'..".format(command))


def show_help():
    print('use [item] [target],  interact [object],  inventory,  move [direction],  bash [object]')
    pass


def use(this, that):
    print('Use is not implemented')


def interact(obj):
    print('Interact is not implemented')


def inventory():
    print('Inventory is not implemented')


def move(direction):
    print('Move is not implemented')


def bash():
    print('Bash is not implemented')


def change_area(direction):
    if player.Player.move(direction):
        p_y, p_x = player.Player.get_position()
        world.world_map[p_y][p_x].describe()
        pass
    else:
        pass


def play():
    """
    placeholder
    """

    control()

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