#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
import items


class Area:
    """
    placeholder
    """
    items = None
    name = None  # Debug purposes
    blocked = None  # Blocked exits

    def __init__(self, _items, name=None, blocked=None):
        self.items = _items
        self.name = name
        self.blocked = blocked

    def __str__(self):
        return 'Area::name={0}, blocked={1}, items={2}'.format(self.name, self.blocked, self.items)


# Forest
forest01 = Area(None, 'forest01')
forest02 = Area(None, 'forest02')
forest03 = Area([items.itemlist['axe']], 'forest03', ['north'])
forest04 = Area(None, 'forest04')
forest05 = Area(None, 'forest05')

worldmap = [[forest01, forest02, None],
            [forest03, forest04, forest05]]