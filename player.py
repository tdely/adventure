#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
import world


class Player:
    """
    The 'player character'
    """
    def __init__(self, position):
        self.y, self.x = position
        self.inventory = []

    def __str__(self):
        return 'Player::position={0}, inventory={1}'.format(self.position, self.inventory)

    def get_position(self):
        """
        Get position of player
        :return: y and x coordinates
        """
        return self.y, self.x

    def get_inventory(self):
        """
        Get inventory of player
        :return: self.inventory
        """
        return self.inventory

    def has_item(self, target):
        """
        Check if item is in inventory
        :param target: item in inventory
        :return: True on success, else False
        """
        for item in self.inventory:
            if target == item.name:
                return True
        return False

    def get_item(self, target):
        """
        Get an item from inventory
        :param target: item in inventory
        :return: item on success, else False
        """
        for item in self.inventory:
            if target == item.name:
                return item
        return False

    def move(self, direction):
        """
        Change player position
        :param direction: direction to move
        :return: True on success, else False
        """
        if direction not in world.world_map[self.y][self.x].blocked:
            d_y, d_x = world.Direction[direction].value
            self.y += d_y
            self.x += d_x
            return True
        return False