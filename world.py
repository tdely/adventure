#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
from items import furniture_list as i
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
        :rtype : bool
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
fs01 = Area([i['fs01_boulder'], i['fs01_tree'], i['fs01_axe']], 'forest01', ['south', 'east'], 'F0.0')
fs02 = Area(None, 'forest02', ['west'], 'F0.1')
fs03 = Area(None, 'forest03', ['north'], 'F1.0')
fs04 = Area(None, 'forest04', None, 'F1.1')
fs05 = Area(None, 'forest05', None, 'F1.2')
fs06 = Area(None, 'forest06', None, 'F2.0')
fs07 = Area(None, 'forest07', None, 'F2.1')
fs08 = Area(None, 'forest08', None, 'F2.2')
fs09 = Area(None, 'forest09', None, 'F3.0')
fs10 = Area(None, 'forest10', None, 'F3.1')
fs11 = Area(None, 'forest11', None, 'F3.2')

start_area = (0, 0)

world_map = [[fs01, fs02, None],
             [fs03, fs04, fs05],
             [fs06, fs07, fs08],
             [fs09, fs10, fs11], ]