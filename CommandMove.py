# -*- coding: utf8 -*-

from CommandAbstract import CommandAbstract
from CommandException import CommandException


class CommandMove(CommandAbstract):
    def run(self):
        if len(self._args) == 0:
            raise CommandException("Where shall I go")

        direction = self._args[0]
        if direction not in ("north", "east", "south", "west"):
            raise CommandException("%s is not a valid direction" % direction)

        #~ Get the area to go from the player (current area) and the direction
