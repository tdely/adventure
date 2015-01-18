#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
import items
from enum import Enum

world_map = []


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
    def __init__(self, _items, name, blocked, description):
        self.items = _items if _items is not None else []
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
        :rtype : bool
        """
        print(self.description)
        for i in self.items:
            item = items.furniture_list[i]
            print('{0}'.format(item.description))

        for direction in ('north', 'west', 'south', 'east'):
            if direction not in self.blocked:
                print('There is an exit {0}.'.format(direction))

    def get_position(self):
        """
        Get area position in world_map
        :rtype : list
        """
        y = 0
        for row in world_map:
            try:
                return [y, row.index(self)]
            except ValueError:
                y += 1
        raise Exception('Area not in world_map')

    def save_position(self):
        """
        Save area position in world_map internally as coordinates
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
                if world_map[adj_y][adj_x] is not None:
                    return True
            except IndexError:
                return False
        return False

    def unblock_exit(self, direction):
        """
        Unblock an exit.
        :rtype : bool
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
                            inv_y, inv_x = Direction[direction].value
                            inv_y *= -1
                            inv_x *= -1
                            inv_direction = Direction.tostring((inv_y, inv_x))
                            world_map[adj_y][adj_x].blocked.remove(inv_direction)
                            return True
                    except IndexError:
                        return False
                return False

        return True

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
    :rtype : None
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
forest01 = Area(['rock', 'tree'], 'forest01', ['south'], 'F0.0')
forest02 = Area(None, 'forest02', None, 'F0.1')
forest03 = Area(None, 'forest03', ['north', 'south'], 'F1.0')
forest04 = Area(None, 'forest04', None, 'F1.1')
forest05 = Area(None, 'forest05', None, 'F1.2')

start_area = (0, 0)

world_map = [[forest01, forest02, None],
             [forest03, forest04, forest05]]