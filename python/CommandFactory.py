# -*- coding: utf8 -*-

class CommandFactory:

    @staticmethod
    def create(player, commandFull):
        cmd = commandFull[0]
        del commandFull[0]

        if cmd == "talk":
            if not player.isConnected() or not player.connect():
                raise "A player must be connected to launch the command talk"
            command = CommandTalk()
        elif cmd == "createPlayer":
            if player.isConnected():
                raise "There must not be a connected player to create a new player"
        else:
            return None

        command.setArgs(commandFull)
        command.setPlayer(player)
        return command;
