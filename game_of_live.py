#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
pymlgame - example game
=======================

This example shows how a simple pymlgame could be written. You also need a connected controller to actually see
something happening. You can use the controller example for this.
"""
import random

from collections import Counter

import math

__author__ = 'Ricardo Band'
__copyright__ = 'Ricardo Band'
__credits__ = ['Ricardo Band']
__license__ = 'MIT'
__version__ = '0.3.1'
__maintainer__ = 'Ricardo Band'
__email__ = 'email@ricardo.band'
__status__ = 'Development'

from datetime import datetime

import pymlgame
from pymlgame.locals import WHITE, BLUE, GREEN, CYAN, MAGENTA, YELLOW, RED, BLACK, E_NEWCTLR, E_DISCONNECT, E_KEYDOWN, E_KEYUP, E_PING
from pymlgame.screen import Screen
from pymlgame.clock import Clock
from pymlgame.surface import Surface


class Game(object):
    """
    The main game class that holds the gameloop.
    """
    def __init__(self, host, port, width, height):
        """
        Create a screen and define some game specific things.
        """
        self.host = host
        self.port = port
        self.width = width
        self.height = height

        self.players = {}

        pymlgame.init()
        self.screen = Screen(self.host, self.port,
                             self.width, self.height)
        self.clock = Clock(15)
        self.running = True
        self.colors = [WHITE, BLUE, GREEN, CYAN, MAGENTA, YELLOW, RED]
        self.color_length = math.ceil(self.screen.height / len(self.colors))

        # surfaces
        self.game_board = [0 for _ in range(self.screen.height * self.screen.width)]
        indices = random.sample(range(self.screen.height * self.screen.width), random.randint(self.screen.width // 2, (2 * (self.screen.height * self.screen.width) // 3)))

        for index in indices:
            self.game_board[index] = 1

        self.dots = Surface(self.screen.width, self.screen.height)

    def offset(self, width_idx, height_idx):
        return height_idx * self.screen.width + width_idx

    def board_value(self, width_idx, height_idx):
        if width_idx == -1 or height_idx == -1:
            return 0
        return self.game_board[self.offset(width_idx, height_idx)]

    def update(self):
        """
        Update the screens contents in every loop.
        """
        # this is not really neccesary because the surface is black after initializing
        self.dots.fill(BLACK)

        for h_index in range(self.screen.height):
            for w_index in range(self.screen.width):
                id_above = h_index - 1 if h_index - 1 >= 0 else -1
                id_left = w_index - 1 if w_index - 1 >= 0 else -1
                id_right = w_index + 1 if w_index + 1 < self.screen.width else -1
                id_bottom = h_index + 1 if h_index + 1 <- self.screen.height else -1

                cell_offset = self.offset(w_index, h_index)

                alive_check = [
                    self.board_value(id_left, id_above),
                    self.board_value(w_index, id_above),
                    self.board_value(id_right, id_above),
                    self.board_value(id_left, h_index),
                    self.board_value(w_index, h_index),
                    self.board_value(id_right, h_index),
                    self.board_value(id_left, id_bottom),
                    self.board_value(w_index, id_bottom),
                    self.board_value(id_right, id_bottom),
                ]

                # count neighbours that are alive
                counter = Counter(alive_check)
                num_alive = counter[1]

                if self.game_board[cell_offset] == 0:
                    if num_alive == 3:
                        self.game_board[cell_offset] = 1
                        self.dots.draw_dot((w_index, h_index), self.colors[h_index // self.color_length])
                elif num_alive < 2:
                    self.game_board[cell_offset] = 0
                elif 2 <= num_alive <= 3:
                    self.dots.draw_dot((w_index, h_index), self.colors[h_index // self.color_length])
                else:
                    self.game_board[cell_offset] = 0

    def render(self):
        """
        Send the current screen content to Mate Light.
        """
        self.screen.reset()
        self.screen.blit(self.dots)

        self.screen.update()
        self.clock.tick()

    def handle_events(self):
        """
        Loop through all events.
        """
        for event in pymlgame.get_events():
            if event.type == E_NEWCTLR:
                #print(datetime.now(), '### new player connected with uid', event.uid)
                self.players[event.uid] = {'name': 'alien_{}'.format(event.uid), 'score': 0}
            elif event.type == E_DISCONNECT:
                #print(datetime.now(), '### player with uid {} disconnected'.format(event.uid))
                self.players.pop(event.uid)
            elif event.type == E_KEYDOWN:
                #print(datetime.now(), '###', self.players[event.uid]['name'], 'pressed', event.button)
                self.colors.append(self.colors.pop(0))
            elif event.type == E_KEYUP:
                #print(datetime.now(), '###', self.players[event.uid]['name'], 'released', event.button)
                self.colors.append(self.colors.pop(0))
            elif event.type == E_PING:
                #print(datetime.now(), '### ping from', self.players[event.uid]['name'])
                pass

    def gameloop(self):
        """
        A game loop that circles through the methods.
        """
        try:
            while True:
                self.handle_events()
                self.update()
                self.render()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    GAME = Game('127.0.0.1', 1337, 40, 16)
    #GAME = Game('matelight.cbrp3.c-base.org', 1337, 40, 16)
    GAME.gameloop()
