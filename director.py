#!/usr/bin/env python3
# -*- encoding: utf-8 -*-§
import player
import world
import items

DEBUG = False

world.initialize_world()
actor = player.Player(world.start_area)
actor.inventory.append('axe')


def control():
    """
    Method for player interaction
    """
    rcode = False
    string = input(': ').lower()
    arguments = string.split()
    command = arguments.pop(0)

    options = {'help': show_help,
               'use': use,
               'interact': interact,
               'inventory': inventory,
               'move': move,
               'bash': bash,
               'examine': examine,
               'describe': _enter_area,
               'exit': exit_game, }
    try:
        rcode = options[command](*arguments)
    except KeyError as e:
        print("I don't know what '{0}' is..".format(command))
        print("Debug: KeyError {0}".format(e)) if DEBUG else None
    except TypeError as e:
        print("Too much information.")
        print("Debug: TypeError {0}".format(e)) if DEBUG else None
    return rcode


def show_help():
    """
    List command help
    """
    print('''Commands:
    use [item] [target]
    interact [target]
    inventory
    move [direction]
    bash [target]
    examine
    exit''')


def use(item=None, target=None):
    """
    Use an item on an object
    """
    match = False
    if item is None and target is None:
        print("You reach into your pockets but forgot what you were looking for.")
        return False
    # Does the player have the item?
    for i in actor.get_inventory():
        if item == i:
            match = True
            break

    if not match:
        print("You don't carry '{0}'.".format(item))
        return False

    if target is None:
        print("You reach for '{0}', but forgot what you were going to do.".format(item))
        return False

    y, x = actor.get_position()
    for i in world.world_map[y][x].items:
        if target == i:
            return 'use', item, target

    print("You try to use '{0}' with '{1}', but can't find '{1}'.".format(item, target))
    return False


def interact(target=None):
    """
    Interact with an object
    """
    if target is None:
        print("You can't interact with nothing.")
        return False
    return 'interact', target


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


def bash(target=None):
    """
    Destroy an object
    """
    if target is None:
        print("You swing your fist in the air.")
        return False

    y, x = actor.get_position()
    for i in world.world_map[y][x].items:
        if target == i:
            if items.furniture_list[i].breakable:
                world.world_map[y][x].items.remove(i)
                print("You bash '{0}' to dust.".format(target))
                return 'bash', target
            else:
                print("You bash '{0}' to no effect.".format(target))
                return False

    print("You look for '{0}' intent on breaking it but can't find it.".format(target))
    return False


def examine(target):
    pass


def _enter_area():
    """
    placeholder
    """
    print(chr(27) + '[2J' + chr(27) + '[;H')
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
    while True:
        rcode = control()

        print(rcode) if DEBUG else None

        if rcode is True or rcode is False:
            continue
        if rcode == 'exit':
            break

        generic_fail = 'You try but fail, better think of something else.'

        y, x = actor.get_position()
        command = rcode[0]
        # Area specific events.
        if world.world_map[y][x] is world.fs01:
            if command == 'use':
                if rcode[1] == 'axe' and rcode[2] == 'tree':
                    world.fs01.items.remove('tree')
                    world.fs01.unblock_exit('south')
                    _enter_area()
                else:
                    print(generic_fail)
            elif command == 'bash' in rcode:
                if rcode[1] == 'boulder':
                    world.fs01.unblock_exit('east')
                    _enter_area()
            elif command == 'interact':
                print(generic_fail)
        else:
            if command == 'use':
                print(generic_fail)
            elif command == 'interact':
                print(generic_fail)