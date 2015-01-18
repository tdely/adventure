#!/usr/bin/env python3
# -*- encoding: utf-8 -*-§
import player
import world
import items

DEBUG = True

world.initialize_world()
actor = player.Player(world.start_area)
actor.inventory.append('axe')


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
               'exit': exit_game,
               'bash': bash, }
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
    """
    List command help
    """
    print('use [item] [target],  interact [object],  inventory,  move [direction],  bash [object]')


def use(item=None, obj=None):
    """
    Use an item on an object
    """
    match = False
    if item is None and obj is None:
        print("You reach into your pockets but forgot what you are looking for.")
        return False
    # Does the player have the item?
    for i in actor.get_inventory():
        if item == i:
            match = True
            break

    if not match:
        print("You don't carry '{0}'.".format(item))
        return False

    if obj is None:
        print("You reach for '{0}', but forgot what you were going to do.".format(item))
        return False

    y, x = actor.get_position()
    for i in world.world_map[y][x].items:
        if obj == i:
            print('Use is not implemented')
            return True

    print("You try to use '{0}' with '{1}', but can't find '{1}'.".format(item, obj))
    return False


def interact(obj=None):
    """
    Interact with an object
    """
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
        for i in actor.get_inventory():
            print('{0}: {1}'.format(i, items.trinket_list[i].description))
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
        _enter_area()
        return True
    print("You can't move {0}.".format(direction))
    return False


def bash(obj=None):
    """
    Destroy an object
    """
    if obj is None:
        print("You swing your fist in the air.")
        return False

    y, x = actor.get_position()
    for i in world.world_map[y][x].items:
        if obj == i:
            if items.furniture_list[i].breakable:
                world.world_map[y][x].items.remove(i)
                print("You bash '{0}' to dust.".format(obj))
                return True
            else:
                print("You bash '{0}' to no effect.".format(obj))
                return False

    print("You look for '{0}' intent on breaking it but can't find it.".format(obj))
    return False


def _enter_area():
    """
    placeholder
    """
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
    _enter_area()
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