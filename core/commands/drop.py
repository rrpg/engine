# -*- coding: utf-8 -*-

from models import item, area
import core.command
from core.localisation import _

class drop(core.command.command):
	def run(self):
		"""
		c.run()

		Drop an item being in the inventory. The item will be let on the floor
		of the player's current area.
		"""
		# Check an item to drop is provided
		if len(self._args) == 0:
			raise core.command.exception(_('ERROR_DROP_NO_ITEM_GIVEN'))

		# check if a quantity is provided
		if len(self._args) == 1:
			quantity = 1
			name = self._args[0]
		else:
			quantity = int(self._args[0])
			name = self._args[1]

		# Item the player want to drop
		i = item.model.loadBy({'name': name}, ['id_item'])

		if len(i) == 0:
			raise item.exception(_('ERROR_DROP_UNKNOWN_ITEM'))

		i = str(i[0]['id_item'])
		inv = self._player.getInventory()
		if i not in inv.keys():
			raise item.exception(_('ERROR_DROP_ITEM_NOT_AVAILABLE'))
		elif quantity > inv[i]['quantity']:
			raise item.exception(_('ERROR_DROP_QUANTITY_TOO_HIGH_%s') % name)

		# Drop it
		self._player.removeItemsFromInventory(i)
		area.area.addItems(self._player.getAreaId(), i)

		print(_('DROP_CONFIRMATION_%(quantity)s_%(name)s') % {'quantity': quantity, 'name': name})

	def render(self, data):
		pass
