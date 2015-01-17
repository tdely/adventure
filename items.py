#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


class Item:
    """
    Base class for items
    """
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __str__(self):
        return 'Item::name={0}, description={1}'.format(self.name, self.description)


itemlist = {'axe': Item('Axe', 'a woodcutters axe'),
            'ruby': Item('Ruby', 'a precious red gem')}