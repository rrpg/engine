# -*- coding: utf8 -*-

import Command
from CommandTalk import CommandTalk
from PlayerException import PlayerException
from CommandHelp import CommandHelp

class CommandFactory:

    @staticmethod
    def create(player, commandFull):
        cmd = commandFull[0]
        del commandFull[0]

        if cmd == "talk":
            if not player.isConnected() or not player.connect():
                raise PlayerException("A player must be connected to launch the command talk")
            command = CommandTalk()
        elif cmd == "createPlayer":
            if player.isConnected():
                raise PlayerException("You cannot create a new player when you're connected")
        elif cmd in ('quit', 'exit', 'q'):
            return Command.quit
        elif cmd == 'help':
            command = CommandHelp()
        else:
            return None

        command.setArgs(commandFull)
        command.setPlayer(player)
        return command;
