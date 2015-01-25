#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
from items import furniture_list as f
from enum import Enum

world_map = []


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

    def get_position(self):
        """
        Get area position in world_map
        :return: y and x coordinate
        """
        y = 0
        for row in world_map:
            try:
                return y, row.index(self)
            except ValueError:
                y += 1
        raise Exception('Area not in world_map')

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

    def save_position(self):
        """
        Save area position in world_map internally as coordinates
        :return: True on success, else False
        """
        try:
            self.y, self.x = self.get_position()
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
                if world_map[adj_y][adj_x] is not None:
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
                                world_map[adj_y][adj_x].blocked.remove(inv_direction)
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
                        world_map[adj_y][adj_x].blocked.append(inv_direction)
                        return True
                except IndexError:
                    # Out of bounds on trying to block adjacent area is not a failure
                    return True
            return True
        return True


def initialize_world() -> object:
    """
    Initialize the world.
    """
    for row in world_map:
        for tile in row:
            if tile is not None:
                tile.save_position()

    for row in world_map:
        for tile in row:
            if tile is not None:
                for direction in ('north', 'west', 'south', 'east'):
                    if not tile.exit_available(direction):
                        tile.block_exit(direction)

# Forest
fs01 = Area([f['fs01_axe']], 'forest01', None,
            'fs01')
fs02 = Area([f['fs02_door']], 'forest02', ['south', 'east'],
            'A cave lies to the east.')
fs03 = Area([f['fs03_man'], f['fs03_tree']], 'forest03', ['east', 'south'],
            'A stream blocks the path south. Remains of a bridge lie on both sides of the stream, but there is no way '
            'across anymore.')
fs04 = Area(None, 'forest04', ['west', 'north'],
            'fs04')
fs05 = Area(None, 'forest05', ['north'],
            'A stream lies to the north, a newly felled tree acting as a bridge. A pond blocks any attempt at heading '
            'south.')
fs06 = Area(None, 'forest06', ['east'],
            'fs06')
fs07 = Area(None, 'forest07', None,
            'A pond blocks any attempt at heading west.')
fs08 = Area(None, 'forest08', ['east'],
            'fs08')
cv01 = Area(None, 'cave01', ['west'],
            'It is a damp cave, the only light coming from the west doorway, facing the forest.')
cv02 = Area(None, 'cave02', None,
            'It is a damp cave, the only light is coming from the west.')
cv03 = Area(None, 'cave03', ['south'],
            'It is a dark and damp cave, there is little light escaping this far in.')
cv04 = Area(None, 'cave04', ['south'],
            'It is a dark and damp cave, there is little light escaping this far in.')
cv05 = Area([f['cv05_chest']], 'cave05', ['north', 'south'],
            'It is a dark and damp cave, it is nearly pitch black.')
mt01 = Area(None, 'mountain01', ['west'],
            'mt01')
mt02 = Area(None, 'mountain02', ['east', 'north'],
            'mt02')
mt03 = Area(f['mt03_altar'], 'mountain03', ['west', 'north'],
            'mt03')
mt04 = Area(None, 'mountain04', ['west'],
            'mt04')
mt05 = Area(None, 'mountain05', None,
            'mt04')

start_area = (0, 0)

world_map = [[fs01, fs02, cv01, cv02, cv03],
             [fs03, fs04, None, cv04, cv05],
             [fs05, fs06, mt01, mt02, mt03],
             [None, fs07, fs08, mt04, mt05], ]