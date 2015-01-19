#!/usr/bin/env python3
# -*- encoding: utf-8 -*-§
import player
import world
from items import trinket_list as t, furniture_list as f

DEBUG = False

world.initialize_world()
actor = player.Player(world.start_area)
# actor.inventory.append(t['axe'])


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
               'take': take,
               'drop': drop,
               'examine': examine,
               'search': search,
               'describe': describe,
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
    take [item]
    drop [item]
    examine [target]
    exit''')

# START PLAYER ACTIONS


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
        if item == i.name:
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
        if target == i.name:
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
        for item in actor.get_inventory():
            print('{0}: {1}'.format(item.name, item.description))
    else:
        print('Your inventory is empty.')
    return 'inventory'


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


def bash(target=None):
    """
    Destroy an object
    """
    if target is None:
        print("You swing your fist in the air.")
        return False

    y, x = actor.get_position()
    for item in world.world_map[y][x].items:
        if target == item.name:
            if item.breakable:
                world.world_map[y][x].items.remove(item)
                print("You bash '{0}' to dust.".format(target))
                return 'bash', target
            else:
                return 'bash', target

    print("You look for '{0}' intent on breaking it, but can't find it.".format(target))
    return False


def take(item=None):
    if item is None:
        print('You grab at the air, looking mighty stupid.')
        return False

    y, x = actor.get_position()
    for i in world.world_map[y][x].items:
        if item == i.name and i.obtainable is True:
            world.world_map[y][x].items.remove(i)
            actor.inventory.append(i)
            print('You pick up {0}.'.format(item))
            return 'take', item
    print("There is no {0}.".format(item))
    return False


def drop(item=None):
    """
    Place an item on the ground
    """
    if item is None:
        print('You drop to the ground, feeling confused.')
        return False

    for i in actor.get_inventory():
        if item == i.name:
            y, x = actor.get_position()
            actor.inventory.remove(i)
            world.world_map[y][x].items.append(i)
            print('You drop {0} on the ground.'.format(item))
            return 'drop', 'item'
    print("You don't have {0}.".format(item))
    return False


def examine(target=None):
    if target is None:
        print('Taking a step back and looking at the situation, you find yourself in doubt.')
        return False
    y, x = actor.get_position()
    for item in world.world_map[y][x].items:
        if target == item.name:
            print(item.detail)
            return 'examine', target
    print("You found no '{0}' to examine.".format(target))
    return False


def search():
    y, x = actor.get_position()
    print('You search the area for anything of interest.')
    for item in world.world_map[y][x].items:
        print('You found {0}.'.format(item.name))
    return 'search'

# END PLAYER ACTIONS


def describe():
    """
    placeholder
    """
    print(chr(27) + '[2J' + chr(27) + '[;H')
    y, x = actor.get_position()
    world.world_map[y][x].describe()


def enter_area():
    describe()


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
    while True:
        rcode = control()

        print(rcode) if DEBUG else None

        if rcode is True or rcode is False:
            continue
        if rcode == 'exit':
            break

        generic_fail = 'You try but fail, better think of something else.'
        bash_fail = "You vigorously bash '{0}', but to no effect."

        y, x = actor.get_position()
        command = rcode[0]
        # Area specific events.
        if world.world_map[y][x] is world.fs01:
            if command == 'use':
                if rcode[1] == 'axe' and rcode[2] == 'tree':
                    world.fs01.items.remove(f['fs01_tree'])
                    world.fs01.unblock_exit('south')
                    describe()
                    print('The tree falls, clearing the path south.')
                else:
                    print(generic_fail)
            elif command == 'bash' in rcode:
                if rcode[1] == 'boulder':
                    world.fs01.unblock_exit('east')
                    describe()
                else:
                    print(bash_fail.format(rcode[1]))
            elif command == 'take':
                if rcode[1] == 'axe':
                    if f['fs01_axe'] in actor.inventory:
                        actor.inventory.remove(f['fs01_axe'])
                        actor.inventory.append(t['axe'])

        else:
            if command == 'use':
                print(generic_fail)
            elif command == 'interact':
                print(generic_fail)

    print('Thank you for playing!')