# -*- coding: utf8 -*-

from Player import Player
from CommandFactory import CommandFactory

class Rpg:
    def __init__(self, login, password, action):
        if login != None and password != None:
            print 'rpg created for user ' + login
            print password
            print action
