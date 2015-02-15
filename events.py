#!/usr/bin/env python3
"""
Event handling
"""
from items import trinket_list as t, furniture_list as f
from quests import quest_list
import tictactoe

DEBUG = False


class Event:
    """
    Default events
    """
    @classmethod
    def parse(cls, args, actor, area):
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
        options[args[0]](args, actor, area)

    @staticmethod
    def use(args, actor, area):
        """
        Default on use
        """
        print('You try but fail, better think of something else.')

    @staticmethod
    def bash(args, actor, area):
        """
        Default on bash
        """
        item = area.get_item(args[1])
        if item.breakable:
            area.items.remove(item)
            print("You bash '{0}' to dust.".format(args[1]))
        else:
            print('You vigorously bash {0}, but to no effect.'.format(args[1]))

    @staticmethod
    def take(args, actor, area):
        """
        Default on take
        """
        pass

    @staticmethod
    def interact(args, actor, area):
        """
        Default on interact
        """
        print("You can't seem to figure out how to interact with {0}.".format(args[1]))

    @staticmethod
    def inventory(args, actor, area):
        """
        Default on inventory
        """
        pass

    @staticmethod
    def drop(args, actor, area):
        """
        Default on drop
        """
        pass

    @staticmethod
    def examine(args, actor, area):
        """
        Default on examine
        """
        pass

    @staticmethod
    def search(args, actor, area):
        """
        Default on search
        """
        print("You found nothing.") if not args[1] else None

    @staticmethod
    def describe(args, actor, area, previous=None):
        """
        Default on describe
        """
        print(chr(27) + '[2J' + chr(27) + '[;H')
        print(previous + '\n') if previous is not None else None
        print(area.name) if DEBUG else None
        area.describe()


class Forest01Event(Event):
    """
    Forest01 events
    """
    @staticmethod
    def take(args, actor, area):
        """
        On take
        """
        if args[1] == 'axe':
            if f['fs01_axe'] in actor.inventory:
                actor.inventory.remove(f['fs01_axe'])
                actor.inventory.append(t['axe'])
        else:
            Event.take(args, actor, area)


class Forest02Event(Event):
    """
    Forest02 events
    """
    @staticmethod
    def use(args, actor, area):
        """
        On use
        """
        if args[1] == 'axe' and args[2] == 'door':
            area.items.remove(f['fs02_door'])
            area.unblock_exit('east')
            Event.describe(args, actor, area, 'The door breaks, allowing access to the cave.')
        else:
            Event.use(args, actor, area)


class Forest03Event(Event):
    """
    Forest03 events
    """
    @staticmethod
    def use(args, actor, area):
        """
        On use
        """
        if args[1] == 'axe' and args[2] == 'tree':
            area.items.remove(f['fs03_tree'])
            area.unblock_exit('south')
            area.description = 'A stream blocks the path south. Remains of a bridge lie on both sides of the ' \
                               'stream. A newly felled tree bridges the stream.'
            Event.describe(args, actor, area, 'The tree falls over the stream, providing a path across.')
        else:
            Event.use(args, actor, area)

    @staticmethod
    def interact(args, actor, area):
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
                    print('Well met. Had any luck with your task?')
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
            Event.interact(args, actor, area)


class Forest04Event(Event):
    """
    Forest04 events
    """
    @staticmethod
    def search(args, actor, area):
        """
        On search
        """
        secret = quest_list['blood and ashes']
        if secret.stage == 0:
            area.items.append(f['fs04_pot'])
            secret.accept()
            print('You found pot.')
        else:
            Event.search(args, actor, area)


class Cave03Event(Event):
    """
    Cave03 events
    """
    @staticmethod
    def bash(args, actor, area):
        if args[1] == 'barrel':
            area.items.remove(f['cv03_barrel'])
            area.items.append(t['key'])
            Event.describe(args, actor, area, 'The barrel falls apart as your fist crashes through the brittle wood. '
                                              ' A key lands among the debris.')
        else:
            Event.bash(args, actor, area)

    @staticmethod
    def interact(args, actor, area):
        if args[1] == 'game':
            if tictactoe.play() == 0 and quest_list['player of games'].stage != 2:
                player = quest_list['player of games']
                player.counter += 1
                if player.counter == 1:
                    player.describe()
                    player.accept()
                elif player.counter == 2:
                    player.describe()
                elif player.counter == 3:
                    player.complete(actor.get_inventory())
                    area.items.append(f['cv03_medallion'])
                    Event.describe(args, actor, area, player.describe())

    @staticmethod
    def take(args, actor, area):
        if args[1] == 'medallion':
            if f['cv03_medallion'] in actor.inventory:
                actor.inventory.remove(f['cv03_medallion'])
                actor.inventory.append(t['medallion'])


class Cave04Event(Event):
    """
    Cave03 events
    """
    @staticmethod
    def use(args, actor, area):
        if args[1] == 'key' and args[2] == 'door':
            if f['cv04_locked-door'] in area.items:
                area.items.remove(f['cv04_locked-door'])
                area.items.append(f['cv04_unlocked-door'])
                Event.describe(args, actor, area, 'You unlock the door. ')
            elif f['cv04_unlocked-door'] in area.items:
                area.items.remove(f['cv04_unlocked-door'])
                area.items.append(f['cv04_locked-door'])
                Event.describe(args, actor, area, 'You lock the door. ')
            elif f['cv04_opened-door'] in area.items:
                print("You can't lock an open door.")
        else:
            Event.bash(args, actor, area)

    @staticmethod
    def interact(args, actor, area):
        if args[1] == 'door':
            if f['cv04_locked-door'] in area.items:
                print('The door is locked.')
            elif f['cv04_unlocked-door'] in area.items:
                area.items.remove(f['cv04_unlocked-door'])
                area.items.append(f['cv04_opened-door'])
                area.unblock_exit('east')
                Event.describe(args, actor, area, 'You open the door.')
            elif f['cv04_opened-door'] in area.items:
                area.items.remove(f['cv04_opened-door'])
                area.items.append(f['cv04_unlocked-door'])
                area.block_exit('east')
                Event.describe(args, actor, area, 'You open the door.')


class Cave05Event(Event):
    """
    Cave05 events
    """
    @staticmethod
    def bash(args, actor, area):
        """
        On bash
        """
        if args[1] == 'chest':
            area.items.remove(f['cv05_chest'])
            area.items.append(f['cv05_hammer'])
            Event.describe(args, actor, area, 'The chest breaks under the barrage of your mighty fist.')
        else:
            Event.bash(args, actor, area)

    @staticmethod
    def take(args, actor, area):
        """
        On take
        """
        if args[1] == 'hammer':
            if f['cv05_hammer'] in actor.inventory:
                actor.inventory.remove(f['cv05_hammer'])
                actor.inventory.append(t['hammer'])
        else:
            Event.take(args, actor, area)


class Mountain03Event(Event):
    """
    Mountain03 events
    """
    @staticmethod
    def use(args, actor, area):
        """
        On use
        """
        if args[1] == 'ruby' and args[2] == 'altar':
            actor.inventory.remove(t['ruby'])
            area.items.append(f['mt03_ruby'])
            Event.describe(args, actor, area, 'You place the ruby upon the altar.')
        elif args[1] == 'hammer' and args[2] == 'ruby':
            area.items.remove(f['mt03_ruby'])
            area.items.append(f['mt03_ashes'])
            Event.describe(args, actor, area, 'You bring down the hammer, smashing the gem. A brilliant flash'
                                              'accompanied by a screech emanates from the stone.')
        elif args[1] == 'pot' and args[2] == 'ashes':
            area.items.remove(f['mt03_ashes'])
            actor.inventory.append(t['ashes'])
            Event.describe(args, actor, area, 'You scoop the ashes from the altar into the pot.')
        else:
            Event.use(args, actor, area)


class Mountain05Event(Event):
    """
    Mountain05 events
    """
    @staticmethod
    def search(args, actor, area):
        """
        On search
        """
        if 'north' in area.blocked:
            area.unblock_exit('north')
            area.description = 'The winding mountain path comes to an end, strange markings scattered across the the ' \
                               'rock walls. You can make out a hidden opening into the mountain.'
            Event.describe(args, actor, area, 'You spot a previously unseen opening into the mountain.')
