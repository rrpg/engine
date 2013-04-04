# -*- coding: utf8 -*-

from CommandAbstract import CommandAbstract
from CommandException import CommandException
from area import area


class CommandMove(CommandAbstract):
	def run(self):
		if len(self._args) == 0:
			raise CommandException("Where shall I go ?")

		direction = self._args[0]
		if direction not in ("north", "east", "south", "west"):
			raise CommandException("%s is not a valid direction" % direction)

		a = area.getByIdCharacterAndDirection(
			self._player._model.getIdCharacter(), direction
		)

		if a is None:
			raise CommandException('I cannot go there')
		else:
			self._player.goTo(a._model.getPk())
			print('lets go %s' % direction)
		#~ Get the area to go from the player (current area) and the direction
