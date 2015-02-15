#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
Quests
"""
from items import trinket_list as t


class Quest:
    """
    Quest or similar trackable task
    """
    def __init__(self, intro, progress, complete, lock=False, required_items=None):
        self.lock = lock
        self.stage = 0
        self.counter = 0  # Optional multipurpose counter
        self.required_items = required_items if required_items is not None else []
        self.dialog_intro = intro
        self.dialog_progress = progress
        self.dialog_complete = complete

    def describe(self):
        """
        Print quest stage description
        """
        if self.stage == 0:
            print(self.dialog_intro)
        elif self.stage == 1:
            print(self.dialog_progress)
        elif self.stage == 2:
            print(self.dialog_complete)

    def accept(self):
        """
        Mark quest as in progress
        :return: True on success, else False
        """
        if self.stage == 0:
            self.stage = 1
            return True
        else:
            return False

    def complete(self, inventory):
        """
        Mark quest as complete
        :return: True on success, else False
        """
        if self.stage == 1:
            if self.validate_required_items(inventory):
                self.stage = 2
                return True
        return False

    def get_required_items(self):
        """
        Get list of required items
        :return: self.required_items
        """
        return self.required_items

    def validate_required_items(self, inventory):
        """
        Check if player has required items
        :param inventory: player inventory
        :return: True or False
        """
        for item in self.required_items:
            if item not in inventory:
                return False
        return True


quest_list = {
    'a woodland riddle': Quest(
        'Greetings! I was wondering when a soul would pass by. I fancy myself a bit of a riddle maker, care to take on '
        'a challenge?',
        'I am the beginning of the end, the end of every place.\n'
        'I am the beginning of eternity, the end of time and space.\n'
        'What am I?',
        "You sure got a head on those shoulders, boy.. Say, you wouldn't mind helping an old man out, would you?."
        "There is an old place of worship up in the mountains, I need you to go there. Find the altar and smash this "
        "gem. Can't do it my self, someone like me can't traverse the harsh path."),
    'player of games': Quest(
        'You sense a slight change in the atmosphere.',
        'A chill runs down your spine.',
        "You notice a medallion next to the board, you could swear it wasn't there a moment ago."),
    'blood and ashes': Quest(
        'None',
        'If you find something.. peculiar, please let me know.',
        "Thank you, son. I bid you adieu.",
        required_items=[t['ashes']]), }
