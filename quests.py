#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


class Quest:
    """
    placeholder
    """
    def __init__(self, intro, progress, complete, lock=False, required_items=None):
        self.lock = lock
        self.stage = 0
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
        """
        if self.stage == 0:
            self.stage = 1
            return True
        else:
            return False

    def complete(self):
        """
        Mark quest as complete
        """
        if self.stage == 1:
            self.stage = 2
            return True
        else:
            return False

    def get_required_items(self):
        return self.required_items


quest_list = {'a woodland riddle': Quest('introduction',
                                         'progress',
                                         'complete'), }