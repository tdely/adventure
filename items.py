#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


class Item:
    """
    Base class for items
    """

    def __init__(self, name, description, detail, breakable, obtainable, interactable):
        self.name = name
        self.description = description
        self.detail = detail
        self.breakable = breakable
        self.obtainable = obtainable
        self.interactable = interactable

    def __str__(self):
        return 'Item::name={0}, description={1}, breakable={2}, interactable={3}'.format(self.name,
                                                                                         self.description,
                                                                                         self.breakable,
                                                                                         self.interactable)


class Furniture(Item):
    """
    Non-inventory item
    """
    def __init__(self, name, description, detail, breakable, interactable, obtainable=False):
        super().__init__(name, description, detail, breakable, obtainable, interactable)


class Trinket(Item):
    """
    Inventory item
    """
    def __init__(self, name, description, detail):
        super().__init__(name, description, detail, breakable=False, obtainable=True, interactable=False)


furniture_list = {'fs01_boulder': Furniture('boulder', 'A boulder blocks the path east.',
                                            'The boulder looks cracked and brittle.',
                                            breakable=True, interactable=False, obtainable=False),
                  'fs01_tree': Furniture('tree', 'A medium sized tree blocks the path south.',
                                         'A perfect tree for woodcutting practice if there ever was one.',
                                         breakable=False, interactable=False, obtainable=False),
                  'fs01_axe': Furniture('axe', 'An old woodcutters axe sits buried in a tree stump.',
                                        "The axe looks like it's been left here for a long time.",
                                        breakable=False, interactable=False, obtainable=True), }

trinket_list = {'axe': Trinket('axe', 'A worn and rusted woodcutters axe.',
                               'It looks abandoned, you feel a sting of guilt.'),
                'ruby': Trinket('ruby', 'A precious red gem.',
                                'Greed is good.'), }