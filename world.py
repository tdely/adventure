#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
import items
from enum import Enum

worldmap = []


class Direction(Enum):
    north = (-1, 0)
    west = (0, -1)
    south = (1, 0)
    east = (0, 1)


class Area:
    """
    placeholder
    """
    items = None
    x = None
    y = None
    name = None  # Debug purposes
    blocked = []  # Blocked exits

    def __init__(self, _items, name, blocked):
        self.items = _items
        self.name = name
        self.blocked = blocked

    def __str__(self):
        return 'Area::name={0}, blocked={1}, pos={2},{3}'.format(self.name, self.blocked, self.y, self.x)

    def get_position(self):
        """
        Get area position in worldmap
        :rtype : list
        """
        y = 0
        for row in worldmap:
            try:
                return [y, row.index(self)]
            except ValueError:
                y += 1
                pass
        raise Exception('Area not in worldmap')

    def save_position(self):
        """
        Save area position in worldmap internally as coordinates
        :rtype : bool
        """
        try:
            self.y, self.x = self.get_position()
            return True
        except TypeError:
            return False

    def exit_available(self, direction):
        """
        Check if an exit is available
        :rtype : bool
        """
        new_y, new_x = Direction[direction].value
        # print(self.y, self.x)
        # print(new_y, new_x)
        new_y += self.y
        new_x += self.x
        # print('{0} y{1}x{2}'.format(direction, new_y, new_x))
        if new_y >= 0 and new_x >= 0:
            try:
                if worldmap[new_y][new_x] is not None:
                    return True
            except IndexError:
                return False
        return False

    def unblock_exit(self, direction):
        """
        Unblock an exit.
        :rtype : bool
        """
        if direction in self.blocked:
            new_y, new_x = Direction[direction].value
            new_y += self.y
            new_x += self.x
            if new_y >= 0 and new_x >= 0:
                try:
                    if worldmap[new_y][new_x] is not None:
                        self.blocked.remove(direction)
                        return True
                except IndexError:
                    return False
        return False

    def block_exit(self, direction):
        """
        Block an exit.
        :rtype : bool
        """
        if direction not in self.blocked:
            self.blocked.append(direction)
            return True
        return False


def initialize_world() -> object:
    """
    Initialize the world.
    :rtype : None
    """
    for row in worldmap:
        for i in row:
            if i is not None:
                i.save_position()

    for row in worldmap:
        for tile in row:
            if tile is not None:
                for direction in ('north', 'west', 'south', 'east'):
                    if not tile.exit_available(direction):
                        tile.block_exit(direction)

# Forest
forest01 = Area(None, 'forest01', [])
forest02 = Area(None, 'forest02', [])
forest03 = Area(None, 'forest03', ['north', 'south'])
forest04 = Area(None, 'forest04', [])
forest05 = Area(None, 'forest05', [])

worldmap = [[forest01, forest02, None],
            [forest03, forest04, forest05]]