#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
The main file.
Commands and events
"""
import player
import world
from quests import quest_list
from items import trinket_list as t, furniture_list as f

DEBUG = False

world.initialize_world()
actor = player.Player(world.start_area)


def control():
    """
    Method for player interaction
    """
    rcode = False
    string = input(': ').lower()
    arguments = string.split()
    command = arguments.pop(0)

    options = {'help': show_help,
               'h': show_help,
               'use': use,
               'u': use,
               'interact': interact,
               'int': interact,
               'inventory': inventory,
               'inv': inventory,
               'move': move,
               'm': move,
               'bash': bash,
               'b': bash,
               'take': take,
               't': take,
               'drop': drop,
               'dr': drop,
               'examine': examine,
               'exa': examine,
               'search': search,
               's': search,
               'describe': describe,
               'de': describe,
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
    u, use [item] [target]
    int, interact [target]
    inv, inventory
    m, move [direction]
    b, bash [target]
    t, take [item]
    dr, drop [item}
    exa, examine [target]
    s, search
    de, describe [target]
    exit''')
    return True

# START PLAYER ACTIONS


def use(item=None, target=None):
    """
    Use an item on an object
    """
    if item is None and target is None:
        print("You reach into your pockets but forgot what you were looking for.")
        return False

    # Does the player have the item?
    if not actor.has_item(item):
        print("You don't carry '{0}'.".format(item))
        return False

    if target is None:
        print("You reach for '{0}', but forgot what you were going to do.".format(item))
        return False

    y, x = actor.get_position()
    if world.world_map[y][x].has_item(target):
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
    y, x = actor.get_position()
    area = world.world_map[y][x]
    if area.has_item(target):
        return 'interact', target
    print("There is no {0}.".format(target))
    return False


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
    return 'inventory', None


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
    area = world.world_map[y][x]
    if area.has_item(target):
            return 'bash', target

    print("You look for '{0}' intent on breaking it, but can't find it.".format(target))
    return False


def take(target=None):
    """
    Pick up an item
    """
    if target is None:
        print('You grab at the air, looking mighty stupid.')
        return False

    y, x = actor.get_position()
    area = world.world_map[y][x]
    if area.has_item(target):
        item = area.get_item(target)
        if item.obtainable:
            area.items.remove(item)
            actor.inventory.append(item)
            print('You pick up {0}.'.format(target))
            return 'take', target
        print("You can't pick up {0}.".format(target))
        return False
    print("There is no {0}.".format(target))
    return False


def drop(target=None):
    """
    Place an item on the ground
    """
    if target is None:
        print('You drop to the ground, feeling confused.')
        return False

    if actor.has_item(target):
        y, x = actor.get_position()
        item = actor.get_item(target)
        actor.inventory.remove(item)
        world.world_map[y][x].items.append(item)
        print('You drop {0} on the ground.'.format(target))
        return 'drop', 'item'
    print("You don't have {0}.".format(target))
    return False


def examine(target=None):
    """
    Inspect an object
    """
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
    """
    Search area for objects
    """
    y, x = actor.get_position()
    print('You search the area for anything of interest.')
    found = False
    for item in world.world_map[y][x].items:
        found = True
        print('You found {0}.'.format(item.name))
    return 'search', found

# END PLAYER ACTIONS


def describe(previous=None):
    """
    Show area description
    """
    print(chr(27) + '[2J' + chr(27) + '[;H')
    print(previous + '\n') if previous is not None else None
    y, x = actor.get_position()
    print(world.world_map[y][x].name) if DEBUG else None
    world.world_map[y][x].describe()
    return 'describe', None


def enter_area():
    """
    Execute 'enter area' procedure
    """
    describe()


def exit_game():
    """
    Exit the game
    """
    confirm = input('Are you sure you want to exit the game? (y/n) ').lower()
    if confirm in ('y', 'yes'):
        return 'exit'
    else:
        print('Continuing game.')
        return False


def events(rcode):
    """
    Call events for correct area
    """
    y, x = actor.get_position()
    current_area = world.world_map[y][x]

    # Area specific events.
    if current_area is world.fs01:
        Forest01Event.parse(rcode)
    elif current_area is world.fs02:
        Forest02Event.parse(rcode)
    elif current_area is world.fs03:
        Forest03Event.parse(rcode)
    elif current_area is world.fs04:
        Forest04Event.parse(rcode)
    elif current_area is world.cv03:
        Cave03Event.parse(rcode)
    elif current_area is world.cv05:
        Cave05Event.parse(rcode)
    elif current_area is world.mt03:
        Mountain03Event.parse(rcode)
    else:
        Event.parse(rcode)


def play():
    """
    Play the game
    """
    enter_area()
    while True:
        if quest_list['blood and ashes'].stage == 2:
            print('You completed the game.')
            break

        rcode = control()

        print(rcode) if DEBUG else None

        if rcode is True or rcode is False:
            continue
        if rcode == 'exit':
            break

        events(rcode)

    print('Thank you for playing!')


class Event:
    """
    Default events
    """
    @classmethod
    def parse(cls, args):
        """
        Pick event to trigger
        """
        options = {'use': cls.use,
                   'bash': cls.bash,
                   'take': cls.take,
                   'interact': cls.interact,
                   'inventory': cls.inventory,
                   'drop': cls.drop,
                   'examine': cls.examine,
                   'search': cls.search,
                   'describe': cls.describe, }
        options[args[0]](args)

    @staticmethod
    def use(args):
        """
        Default on use
        """
        print('You try but fail, better think of something else.')

    @staticmethod
    def bash(args):
        """
        Default on bash
        """
        y, x = actor.get_position()
        area = world.world_map[y][x]
        item = area.get_item(args[1])
        if item.breakable:
            area.items.remove(item)
            print("You bash '{0}' to dust.".format(args[1]))
        else:
            print('You vigorously bash {0}, but to no effect.'.format(args[1]))

    @staticmethod
    def take(args):
        """
        Default on take
        """
        pass

    @staticmethod
    def interact(args):
        """
        Default on interact
        """
        print("You can't seem to figure out how to interact with {0}.".format(args[1]))

    @staticmethod
    def inventory(args):
        """
        Default on inventory
        """
        pass

    @staticmethod
    def drop(args):
        """
        Default on drop
        """
        pass

    @staticmethod
    def examine(args):
        """
        Default on examine
        """
        pass

    @staticmethod
    def search(args):
        """
        Default on search
        """
        print("You found nothing.") if not args[1] else None

    @staticmethod
    def describe(args):
        """
        Default on describe
        """
        pass


class Forest01Event(Event):
    """
    Forest01 events
    """
    @staticmethod
    def take(args):
        """
        On take
        """
        if args[1] == 'axe':
            if f['fs01_axe'] in actor.inventory:
                actor.inventory.remove(f['fs01_axe'])
                actor.inventory.append(t['axe'])
        else:
            Event.take(args)


class Forest02Event(Event):
    """
    Forest02 events
    """
    @staticmethod
    def use(args):
        """
        On use
        """
        if args[1] == 'axe' and args[2] == 'door':
            world.fs02.items.remove(f['fs02_door'])
            world.fs02.unblock_exit('east')
            describe('The door breaks, allowing access to the cave.')
        else:
            Event.use(args)


class Forest03Event(Event):
    """
    Forest03 events
    """
    @staticmethod
    def use(args):
        """
        On use
        """
        if args[1] == 'axe' and args[2] == 'tree':
            world.fs03.items.remove(f['fs03_tree'])
            world.fs03.unblock_exit('south')
            world.fs03.description = 'A stream blocks the path south. Remains of a bridge lie on both sides of the ' \
                                     'stream. A newly felled tree bridges the stream.'
            describe('The tree falls over the stream, providing a path across.')
        else:
            Event.use(args)

    @staticmethod
    def interact(args):
        """
        On interact
        """
        if args[1] == 'man':
            riddle = quest_list['a woodland riddle']
            secret = quest_list['blood and ashes']
            if riddle.stage == 2:
                if secret.stage == 1:
                    if secret.validate_required_items(actor.get_inventory()):
                        answer = input('Trade you that urn of ashes for this here violin, Johnny boy. (y/n)')
                        if answer == 'y':
                            secret.complete(actor.get_inventory())
                            actor.inventory.remove(t['ashes'])
                            secret.describe()
                    else:
                        secret.describe()
                else:
                    print('Well met.')
            if riddle.stage == 0:
                riddle.describe()
                riddle.accept()
            if riddle.stage == 1:
                riddle.describe()
                answer = input('Speak: ').lower()
                if answer == 'e' or answer == 'the letter e':
                    riddle.complete(actor.get_inventory())
                    riddle.describe()
                    actor.inventory.append(t['ruby'])
                else:
                    print('Not quite.')
        else:
            Event.interact(args)


class Forest04Event(Event):
    """
    Forest04 events
    """
    @staticmethod
    def search(args):
        """
        On search
        """
        secret = quest_list['blood and ashes']
        if secret.stage == 0:
            world.fs04.items.append(f['fs04_pot'])
            secret.accept()
            print('You found pot.')
        else:
            Event.search(args)


class Cave03Event(Event):
    """
    Cave03 events
    """
    @staticmethod
    def bash(args):
        if args[1] == 'barrel':
            world.cv03.items.remove(f['cv03_barrel'])
            describe('The barrel falls apart as your fist crashes through the brittle wood.')
        else:
            Event.bash(args)


class Cave05Event(Event):
    """
    Cave05 events
    """
    @staticmethod
    def bash(args):
        """
        On bash
        """
        if args[1] == 'chest':
            world.cv05.items.remove(f['cv05_chest'])
            world.cv05.items.append(f['cv05_hammer'])
            describe('The chest breaks under the barrage of your mighty fist.')
        else:
            Event.bash(args)

    @staticmethod
    def take(args):
        """
        On take
        """
        if args[1] == 'hammer':
            if f['cv05_hammer'] in actor.inventory:
                actor.inventory.remove(f['cv05_hammer'])
                actor.inventory.append(t['hammer'])
        else:
            Event.take(args)


class Mountain03Event(Event):
    """
    Mountain03 events
    """
    @staticmethod
    def use(args):
        """
        On use
        """
        if args[1] == 'ruby' and args[2] == 'altar':
            actor.inventory.remove(t['ruby'])
            world.mt03.items.append(f['mt03_ruby'])
            describe('You place the ruby upon the altar.')
        elif args[1] == 'hammer' and args[2] == 'ruby':
            world.mt03.items.remove(f['mt03_ruby'])
            world.mt03.items.append(f['mt03_ashes'])
            describe('You bring down the hammer, smashing the gem. A brilliant flash accompanied by a screech emanates '
                     'from the stone.')
        elif args[1] == 'pot' and args[2] == 'ashes':
            world.mt03.items.remove(f['mt03_ashes'])
            actor.inventory.append(t['ashes'])
            describe('You scoop the ashes from the altar into the pot.')
        else:
            Event.use(args)
