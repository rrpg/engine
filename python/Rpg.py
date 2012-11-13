# -*- coding: utf8 -*-

class Rpg:
    def __init__(self, login, password, action):
        if login != None and password != None:
            print 'rpg created for user ' + login
            print password
            print action
