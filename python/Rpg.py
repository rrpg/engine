# -*- coding: utf8 -*-

from Player import Player
from CommandFactory import CommandFactory
import Command

class Rpg:
    def __init__(self, login, password, action):
        #if the game is launched with login/password, the player is directly fetched
        if login != None and password != None:
            self._player = Player(login, password)
        elif action == []:
            #else an empty player is created
            self._player = Player(None, None)
            self._doInteractiveAuth()

        self._action = action

        self._player.connect()

    #~ This method asks the player to login or to create a new account
    def _doInteractiveAuth(self):
        choice = 0
        while choice != '1' and choice != '2':
            choice = raw_input("new account (1) or login (2) ? ")

        if choice == '1':
            self._player.createNewPlayerFromStdIn()
        elif choice == '2':
            self._player.loadPlayerFromStdIn()


    #~ Main method of the Rpg Class, will run the action if it is given,
    #~ else ask the player to enter a command
    def run(self):
        if len(self._action) > 0:
            self._runAction()
        else:
            command = ''
            result = 0
            while 1:
                command = raw_input("Command: ")

                if command != "":
                    self._action = command.split(' ')
                    result = self._runAction()

                if result == command.quit:
                    break

    def _runAction(self):
        command = CommandFactory.create(self._player, self._action)
        if command == None:
            raise BaseException("Unknown command")

        return command.run()
