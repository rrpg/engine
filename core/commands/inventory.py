# -*- coding: utf-8 -*-

from models import item
import core.command
from core.localisation import _


class inventory(core.command.command):
	def run(self):
		"""
		c.run()

		Display the player's inventory.
		"""

		i = self._player.getInventory()
		for itemId in i:
			it = item.model.loadById(itemId)
			print(str(i[itemId]['quantity']).rjust(3) + ' ' + it['name'])

	def render(self, data):
		pass
