# -*- coding: utf8 -*-

from CommandAbstract import CommandAbstract
from Character import Character
from AreaModel import AreaModel


class CommandLook(CommandAbstract):
	def run(self):
		# Display surrounding characters
		characters = Character.searchByPlayer(self._player)
		if len(characters) == 0:
			print("You're alone here.")
		else:
			print("Characters arround:")
			for c in Character.searchByPlayer(self._player):
				print(c._model.getName())

		# Display accessible areas
		areas = AreaModel.getSurroundingAreas(self._player._model.getIdArea())
		print("You can go " +
			', '.join(filter(lambda k: areas[k] == 1, areas)) + '.')

		# Display surrounding objects
		#@TODO
