#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
import items
from enum import Enum

worldmap = []


class Direction(Enum):
    """
    Enum of direction
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
    placeholder
    """
    def __init__(self, _items, name, blocked):
        self.items = _items
        self.name = name
        self.x = None
        self.y = None
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
        adj_y, adj_x = Direction[direction].value
        adj_y += self.y
        adj_x += self.x
        if adj_y >= 0 and adj_x >= 0:
            try:
                if worldmap[adj_y][adj_x] is not None:
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
            # Get adjacent area
            adj_y, adj_x = Direction[direction].value
            adj_y += self.y
            adj_x += self.x
            # Only unblock if there is an adjacent area
            if adj_y >= 0 and adj_x >= 0:
                try:
                    if worldmap[adj_y][adj_x] is not None:
                        self.blocked.remove(direction)
                        # Remove block on adjacent area
                        inv_y, inv_x = Direction[direction].value
                        inv_y *= -1
                        inv_x *= -1
                        inv_direction = Direction.tostring((inv_y, inv_x))
                        worldmap[adj_y][adj_x].blocked.remove(inv_direction)
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
            # Get adjacent area
            adj_y, adj_x = Direction[direction].value
            adj_y += self.y
            adj_x += self.x
            # Block from other side if possible
            if adj_y >= 0 and adj_x >= 0:
                try:
                    if worldmap[adj_y][adj_x] is not None:
                        # Remove block on adjacent area
                        inv_y, inv_x = Direction[direction].value
                        inv_y *= -1
                        inv_x *= -1
                        inv_direction = Direction.tostring((inv_y, inv_x))
                        worldmap[adj_y][adj_x].blocked.append(inv_direction)
                        return True
                except IndexError:
                    # Out of bounds on trying to block adjacent area is not a failure
                    return True
            return True
        return False


def initialize_world() -> object:
    """
    Initialize the world.
    :rtype : None
    """
    for row in worldmap:
        for tile in row:
            if tile is not None:
                tile.save_position()

    for row in worldmap:
        for tile in row:
            if tile is not None:
                for direction in ('north', 'west', 'south', 'east'):
                    if not tile.exit_available(direction):
                        tile.block_exit(direction)

# Forest
forest01 = Area(None, 'forest01', ['south'])
forest02 = Area(None, 'forest02', [])
forest03 = Area(None, 'forest03', ['north', 'south'])
forest04 = Area(None, 'forest04', [])
forest05 = Area(None, 'forest05', [])

worldmap = [[forest01, forest02, None],
            [forest03, forest04, forest05]]