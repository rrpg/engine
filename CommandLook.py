# -*- coding: utf8 -*-

from CommandAbstract import CommandAbstract
from character import character
from area import area


class CommandLook(CommandAbstract):
	def run(self):
		# Display surrounding characters
		characters = character.searchByPlayer(self._player)
		if len(characters) == 0:
			print("You're alone here.")
		else:
			print("Characters arround:")
			for c in character.searchByPlayer(self._player):
				print(c._model['name'])

		# Display accessible areas
		areas = area.getSurroundingAreas(self._player._model['id_area'])
		print("You can go " +
			', '.join(filter(lambda k: areas[k] == 1, areas)) + '.')

		# Display surrounding objects
		#@TODO
