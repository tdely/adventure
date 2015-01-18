#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


class Item:
    """
    Base class for items
    """

    def __init__(self, name, description, breakable, obtainable, usable):
        self.name = name
        self.description = description
        self.breakable = breakable
        self.obtainable = obtainable
        self.usable = usable

    def __str__(self):
        return 'Item::name={0}, description={1}, breakable={2}, usable={3}'.format(self.name, self.description,
                                                                                   self.breakable, self.usable)


class Furniture(Item):
    """
    Unobtainable items
    """
    def __init__(self, name, description, breakable, usable):
        self.name = name
        self.description = description
        self.breakable = breakable
        self.usable = usable
        super().__init__(self.name, self.description, self.breakable, False, self.usable)


class Trinket(Item):
    """
    Obtainable item
    """
    def __init__(self, name, description):
        self.name = name
        self.description = description
        super().__init__(self.name, self.description, False, True, False)


furniture_list = {'boulder': Furniture('rock', 'A boulder blocks the path east.', True, False),
                  'tree': Furniture('tree', 'A medium sized tree blocks the path south', False, False), }

trinket_list = {'axe': Trinket('axe', 'a woodcutters axe'),
                'ruby': Trinket('ruby', 'a precious red gem'), }