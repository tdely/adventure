#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
import world


class Player:

    def __init__(self, position):
        self.y, self.x = position
        self.inventory = []

    def __str__(self):
        return 'Player::position={0}, inventory={1}'.format(self.position, self.inventory)

    def get_position(self):
        """
        Get position of player
        :rtype: list
        """
        return self.y, self.x

    def get_inventory(self):
        """
        Get inventory of player
        :rtype: list
        """
        return self.inventory

    def move(self, direction):
        """
        Change player position
        :rtype: bool
        """
        if direction not in world.world_map[self.y][self.x].blocked:
            d_y, d_x = world.Direction[direction].value
            self.y += d_y
            self.x += d_x
            return True
        else:
            return False