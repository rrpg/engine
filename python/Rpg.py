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

    def run(self):
        if ((not self._authenticate and len(self._action) == 0) or self._authenticate):
            #~ try:
            self._player.connect()
            #~ except BaseException, e:
                #~ print e
                #~ return

        if len(self._action) > 0:
            self._runAction()
        else:
            q = False
            command = ''
            while not q:
                print "Command:"
                command = raw_input()

                if command == "quit":
                    q = True
                elif command != "":
                    self._action = command.split(' ')
                    self._runAction()

    def _runAction(self):
        command = CommandFactory.create(self._player, self._action)
        if command != None:
            command.run()
        else:
            print "Unknown command"
            return 0
        return 1
