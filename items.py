#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
Items
"""


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


furniture_list = {'fs01_axe': Furniture('axe', 'An old woodcutters axe sits buried in a tree stump.',
                                        "The axe looks like it's been left here for a long time.",
                                        breakable=False, interactable=False, obtainable=True),
                  'cv03_barrel': Furniture('barrel', 'An old barrel stands in the corner.',
                                           'The barrel appears weak.',
                                           breakable=True, interactable=False, obtainable=False),
                  'fs02_door': Furniture('door', 'A sturdy door blocks the entrance to the cave.',
                                         'The door appears locked. The wood is old and dry, although still solid.',
                                         breakable=False, interactable=False, obtainable=False),
                  'fs04_pot': Furniture('pot', 'An old ceramic pot lies in the undergrowth.',
                                        "It's remarkable that a weak pot has remained unbroken in a place like this.",
                                        breakable=False, interactable=False, obtainable=True),
                  'cv05_chest': Furniture('chest', 'In the corner stands an old dusty chest.',
                                          'It is locked, but appears to have been weakened by prolonged exposure to '
                                          'the humid air.',
                                          breakable=True, interactable=False, obtainable=True),
                  'cv05_hammer': Furniture('hammer', 'An ornate hammer lies among the rubble of the broken chest.',
                                           'A hammer that appears to be of religious or spiritual origin.',
                                           breakable=False, interactable=False, obtainable=True),
                  'fs03_tree': Furniture('tree', 'A medium sized tree stands near the stream.',
                                         'A perfect tree for woodcutting practice if there ever was one.',
                                         breakable=False, interactable=False, obtainable=False),
                  'fs03_man': Furniture('man', 'A sly looking man in a wide brimmed hat sits on a hickory stump, deep '
                                               'in thought and smoking a pipe.',
                                        'Although appearing deep in thought, you get the feeling he is watching you '
                                        'closely.',
                                        breakable=False, interactable=True, obtainable=False),
                  'mt03_altar': Furniture('altar', 'An altar of stone, cut from the mountain, stands before you.',
                                          "There appears.",
                                          breakable=False, interactable=False, obtainable=False),
                  'mt03_ruby': Furniture('ruby', 'The ruby lies upon the altar, it seems different than earlier.',
                                         'Out of the corner of your eyes the gemstone appears to occasionally move or '
                                         'squirm.',
                                         breakable=False, interactable=False, obtainable=False),
                  'mt03_ashes': Furniture('ashes', 'A pile of ashes have taken the place of the ruby on the altar.',
                                          "It's a perplexing thing, a gemstone turning into ashes.",
                                          breakable=False, interactable=False, obtainable=False), }

trinket_list = {'axe': Trinket('axe', 'A worn and rusted woodcutters axe.',
                               'An axe used for cutting down trees.'),
                'ruby': Trinket('ruby', 'A precious red gem.',
                                'Something feels slightly off about this stone.'),
                'hammer': Trinket('hammer', 'A ceremonial hammer.',
                                  'A hammer that appears to be of religious or spiritual origin.'),
                'pot': Trinket('pot', 'An old ceramic pot.',
                               'Perfectly capable of not leaking. Not recommended to carry anything meant for '
                               'consumption.'),
                'ashes': Trinket('ashes', 'A pot containing ashes.',
                                 'Why would a gem turn into ashes when smashed?')}
