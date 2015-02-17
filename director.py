#!/usr/bin/env python3
"""
The main file.
Commands and events
"""
import json
import player
import world
import events
from quests import quest_list
from items import trinket_list as t, furniture_list as f

DEBUG = False

world.initialize_world(world.world_map)
actor = player.Player(world.start_area)


def control():
    """
    Method for player interaction
    """
    rcode = False
    string = input(': ').lower()
    arguments = string.split()

    if len(arguments) == 0:
        return False

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
               'save': save,
               'load': load,
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

        event_handler(rcode)

    print('Thank you for playing!')


def event_handler(rcode):
    """
    Call events for correct area
    """
    y, x = actor.get_position()
    current_area = world.world_map[y][x]

    # Area specific events.
    if current_area is world.fs01:
        events.Forest01Event.parse(rcode, actor, current_area)
    elif current_area is world.fs02:
        events.Forest02Event.parse(rcode, actor, current_area)
    elif current_area is world.fs03:
        events.Forest03Event.parse(rcode, actor, current_area)
    elif current_area is world.fs04:
        events.Forest04Event.parse(rcode, actor, current_area)
    elif current_area is world.cv03:
        events.Cave03Event.parse(rcode, actor, current_area)
    elif current_area is world.cv04:
        events.Cave04Event.parse(rcode, actor, current_area)
    elif current_area is world.cv05:
        events.Cave05Event.parse(rcode, actor, current_area)
    elif current_area is world.mt01:
        events.Mountain01Event.parse(rcode, actor, current_area)
    elif current_area is world.mt02:
        events.Mountain02Event.parse(rcode, actor, current_area)
    elif current_area is world.mt03:
        events.Mountain03Event.parse(rcode, actor, current_area)
    elif current_area is world.mt04:
        events.Mountain04Event.parse(rcode, actor, current_area)
    elif current_area is world.mt05:
        events.Mountain05Event.parse(rcode, actor, current_area)
    else:
        events.Event.parse(rcode, actor, current_area)


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
    save [file -optional]
    load [file -optional]
    exit''')
    return True


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
    if direction not in world.world_map[actor.y][actor.x].blocked:
        d_y, d_x = world.Direction[direction].value
        next_area = world.world_map[actor.y + d_y][actor.x + d_x]
        return 'move', direction, next_area
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


def describe():
    """
    Show area description
    """
    return 'describe', None


def save(target=None):
    """
    Save game to file
    """
    file = target if target is not None else 'quicksave.json'

    # Main dictionary
    save_data = {}

    # Save player specific information
    player_save = {'position': (actor.y, actor.x)}
    item_keys = []
    for key in t:
        for item in actor.inventory:
            if t[key] == item:
                item_keys.append(key)
                continue
    player_save.update({'inventory': item_keys})
    save_data.update({'player': player_save})

    # Save world specific information
    world_save = {}
    for row in world.world_map:
        for tile in row:
            tile_save = {}
            if tile is None:
                continue
            item_keys = []
            for key in t:
                for item in tile.items:
                    if t[key] == item:
                        item_keys.append(key)
                        continue
            for key in f:
                for item in tile.items:
                    if f[key] == item:
                        item_keys.append(key)
                        continue

            tile_save.update({'items': item_keys})
            tile_save.update({'description': tile.description})
            tile_save.update({'coordinates': (tile.y, tile.x)})
            tile_save.update({'blocked': tile.blocked})
            world_save.update({tile.name: tile_save})
    save_data.update({'world': world_save})

    # Save quest specific information
    quest_save = {}
    for key in quest_list:
        quest_save.update({key: {'stage': quest_list[key].stage, 'lock': quest_list[key].lock,
                                 'counter': quest_list[key].counter}})
    save_data.update({'quests': quest_save})

    try:
        json.dump(save_data, open(file, 'w'), indent=4)
        return True
    except IOError:
        print('Save failed: could not write to file.')
    return False


def load(target=None):
    """
    Load game from file
    """
    file = target if target is not None else 'quicksave.json'
    try:
        data = json.load(open(file, 'r'))

        player_data = data['player']
        actor.y, actor.x = player_data['position']
        player_items = []
        for item_name in player_data['inventory']:
            player_items.append(t[item_name])
        actor.inventory = player_items

        world_data = data['world']
        for area in world_data:
            area_items = []
            y, x = world_data[area]['coordinates']
            world.world_map[y][x].description = world_data[area]['description']
            world.world_map[y][x].blocked = world_data[area]['blocked']

            for item_name in world_data[area]['items']:
                if item_name in f:
                    area_items.append(f[item_name])

            for item_name in world_data[area]['items']:
                if item_name in t:
                    area_items.append(t[item_name])
            world.world_map[y][x].items = area_items

        quest_data = data['quests']
        for quest in quest_data:
            quest_list[quest].lock = quest_data[quest]['lock']
            quest_list[quest].stage = quest_data[quest]['stage']
            quest_list[quest].counter = quest_data[quest]['counter']

        enter_area()
    except IOError:
        print('Load failed: could not read file.')
    except ValueError:
        print('Load failed: malformed save.')
    except KeyError:
        print('Load failed: malformed save.')
    return False


def enter_area():
    """
    Execute 'enter area' procedure
    """
    events.Event.describe('describe', actor, world.world_map[actor.y][actor.x])


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
