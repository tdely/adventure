#!/usr/bin/env python3
"""
The world
"""
from items import furniture_list as f
from enum import Enum


class Direction(Enum):
    """
    Directions and corresponding coordinate changes
    """
    north = (-1, 0)
    west = (0, -1)
    south = (1, 0)
    east = (0, 1)

    @classmethod
    def tostring(cls, val):
        """
        Get name from value
        """
        for entry in cls:
            if val == entry.value:
                return entry.name


class Area:
    """
    An area of the playing field
    """
    def __init__(self, item_list, name, blocked, description):
        self.items = item_list if item_list is not None else []
        self.name = name
        self.world = None
        self.x = None
        self.y = None
        self.blocked = blocked if blocked is not None else []
        self.description = description

    def __str__(self):
        return 'Area::name={0}, blocked={1}, pos={2},{3}'.format(self.name, self.blocked, self.y, self.x)

    def describe(self):
        """
        Describe the area
        """
        print(self.description)
        for item in self.items:
            print('{0}'.format(item.description))

        for direction in ('north', 'west', 'south', 'east'):
            if direction not in self.blocked:
                print('There is an exit {0}.'.format(direction))

    def get_position(self, board):
        """
        Get area position in world_map
        :return: y and x coordinate
        """
        y = 0
        for row in board:
            try:
                return y, row.index(self)
            except ValueError:
                y += 1
        raise Exception('Area not in world map')

    def has_item(self, target):
        """
        Check if item is in area
        :param target: item
        :return: True on success, else False
        """
        for item in self.items:
            if target == item.name:
                return True
        return False

    def get_item(self, target):
        """
        Get an item from area
        :param target: item
        :return: item on success, else False
        """
        for item in self.items:
            if target == item.name:
                return item
        return False

    def save_position(self, board):
        """
        Save area position in world_map internally as coordinates
        :return: True on success, else False
        """
        try:
            self.world = board
            self.y, self.x = self.get_position(self.world)
            return True
        except TypeError:
            return False

    def exit_available(self, direction):
        """
        Check if an exit is available
        :return : True on success, else False
        """
        adj_y, adj_x = Direction[direction].value
        adj_y += self.y
        adj_x += self.x
        if adj_y >= 0 and adj_x >= 0:
            try:
                if self.world[adj_y][adj_x] is not None:
                    return True
            except IndexError:
                return False
        return False

    def unblock_exit(self, direction):
        """
        Unblock an exit.
        :return: True on success, else False
        """
        if self.blocked is not None:
            if direction in self.blocked:
                # Get adjacent area
                adj_y, adj_x = Direction[direction].value
                adj_y += self.y
                adj_x += self.x
                # Only unblock if there is an adjacent area
                if adj_y >= 0 and adj_x >= 0:
                    try:
                        if world_map[adj_y][adj_x] is not None:
                            self.blocked.remove(direction)
                            # Remove block on adjacent area
                            try:
                                inv_y, inv_x = Direction[direction].value
                                inv_y *= -1
                                inv_x *= -1
                                inv_direction = Direction.tostring((inv_y, inv_x))
                                self.world[adj_y][adj_x].blocked.remove(inv_direction)
                                return True
                            except ValueError:
                                # The other area is missing a block, not good but not fatal
                                return True
                    except IndexError:
                        return False
                return False

        return True

    def block_exit(self, direction):
        """
        Block an exit.
        :return : True on success, else False
        """
        if direction not in self.blocked:
            self.blocked.append(direction)
            # Get adjacent area
            adj_y, adj_x = Direction[direction].value
            adj_y += self.y
            adj_x += self.x
            # Block from other side if possible
            if adj_y >= 0 and adj_x >= 0:
                try:
                    if world_map[adj_y][adj_x] is not None:
                        # Block from adjacent area
                        inv_y, inv_x = Direction[direction].value
                        inv_y *= -1
                        inv_x *= -1
                        inv_direction = Direction.tostring((inv_y, inv_x))
                        self.world[adj_y][adj_x].blocked.append(inv_direction)
                        return True
                except IndexError:
                    # Out of bounds on trying to block adjacent area is not a failure
                    return True
            return True
        return True


def initialize_world(world):
    """
    Initialize the world.
    """
    for row in world:
        for tile in row:
            if tile is not None:
                tile.save_position(world)

    for row in world:
        for tile in row:
            if tile is not None:
                for direction in ('north', 'west', 'south', 'east'):
                    if not tile.exit_available(direction):
                        tile.block_exit(direction)

# Forest
fs01 = Area([f['fs01_axe']], 'forest01', None,
            'A clearing in the forest, created by logging some time ago if the old tree stumps are anything to go by.')
fs02 = Area([f['fs02_door']], 'forest02', ['south', 'east'],
            'A clearing lies to the west, and a cave lies to the east.')
fs03 = Area([f['fs03_man'], f['fs03_tree']], 'forest03', ['east', 'south'],
            "A stream blocks the path south. Remains of a bridge lie on both sides of the stream, but there's no "
            'longer a way across.')
fs04 = Area(None, 'forest04', ['west', 'north'],
            'The forest is thick as the path ends. A bridge of dubious sturdiness lies across the stream south. The '
            'stream ends in a fall into a chasm to the east.')
fs05 = Area(None, 'forest05', ['north'],
            'A stream lies to the north, a newly felled tree acting as a bridge. A stagnant pond lies south, better not'
            ' get too close..')
fs06 = Area(None, 'forest06', ['east'],
            'The path comes to a crossroads in the thick forest. To the north lies an old bridge across the stream, to '
            'the west the mountain, impassable from here.')
fs07 = Area(None, 'forest07', None,
            'A few rays of sunlight penetrate the forest canopy. A stagnant pond lies west, better not get too close.')
fs08 = Area(None, 'forest08', ['east'],
            'The forest ends with the mountain which lies ahead, impassable except for the path to the north.')
cv01 = Area(None, 'cave01', ['west'],
            'It is a damp cave, the only light coming from the west doorway, facing the forest.')
cv02 = Area(None, 'cave02', None,
            'It is a damp cave, the only light is coming from the west.')
cv03 = Area([f['cv03_barrel'], f['cv03_game']], 'cave03', ['south'],
            'It is a dark and damp cave, there is little light escaping this far in.')
cv04 = Area([f['cv04_locked-door']], 'cave04', ['south', 'east'],
            'It is a dark and damp cave, there is little light escaping this far in.')
cv05 = Area([f['cv05_chest']], 'cave05', ['north', 'south'],
            'It is a dark and damp cave, it is nearly pitch black.')
mt01 = Area(None, 'mountain01', ['west'],
            'Where the forest ends, a mountain path with high walls begin. There are strange markings on the rock. A '
            'chasm lies to the north.')
mt02 = Area(None, 'mountain02', ['east', 'north'],
            'The winding mountain path continues, strange markings scattered across the the rock walls.')
mt03 = Area([f['mt03_altar']], 'mountain03', ['west', 'north'],
            'A spacious cave carved out of the mountain into a hall. Pews line the path to the back of the room.')
mt04 = Area(None, 'mountain04', ['west'],
            'The winding mountain path continues, strange markings scattered across the the rock walls.')
mt05 = Area(None, 'mountain05', ['north'],
            'The winding mountain path comes to a dead end, strange markings scattered across the the rock walls.')

start_area = (0, 0)

world_map = [[fs01, fs02, cv01, cv02, cv03],
             [fs03, fs04, None, cv04, cv05],
             [fs05, fs06, mt01, mt02, mt03],
             [None, fs07, fs08, mt04, mt05], ]
