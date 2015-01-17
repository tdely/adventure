#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
import items


class Area:
    """
    placeholder
    """
    items = None
    exits = None
    name = None  # Debug purposes
    blocked = None  # Blocked exits

    def __init__(self, items, name=None, blocked=None):
        self.items = items
        self.name = name
        self.blocked = blocked

    def __str__(self):
        return 'Area::name={0}, blocked={1}, items={2}'.format(self.name, self.blocked, self.items)

axe = items.Item('Axe', 'a woodcutters axe')
print(axe)

# Forest
forest01 = Area(None, 'forest01')
forest02 = Area(None, 'forest01')
forest03 = Area([items.Item('Axe', 'a woodcutters axe')], 'forest01', ['north'])
forest04 = Area(None, 'forest01')

worldmap = [[forest01, forest02],
            [forest03, forest04], ]