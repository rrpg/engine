# -*- coding: utf8 -*-

from CommandAbstract import CommandAbstract
from CommandException import CommandException


class CommandHelp(CommandAbstract):
    def run(self):
        print('Available commands:')
        print('talk <Character name> "<Sentence>": Talk to a character' +
            ' - Not Yet Implemented')
        print('createPlayer: Not Yet Implemented')
        print('help: Display this help')
        print('quit|exit|q: Quit the game')
