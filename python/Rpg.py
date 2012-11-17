# -*- coding: utf8 -*-

from Player import Player
from CommandFactory import CommandFactory

class Rpg:
    def __init__(self, login, password, action):
        #if the game is launched with login/password, the player is directly fetched
        if login != None and password != None:
            self._player = Player(login, password)
            self._authenticate = True
        #else an empty player is created
        else:
            self._player = Player(None, None)
            self._authenticate = False

        self._action = action

