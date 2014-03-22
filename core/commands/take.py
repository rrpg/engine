# -*- coding: utf-8 -*-

from models import item, area
import core.command
from core.localisation import _


class take(core.command.command):
	def run(self):
		if len(self._args) == 0:
			raise core.command.exception(_('ERROR_TAKE_NO_ITEM_GIVEN'))

		if len(self._args) == 1:
			quantity = 1
			name = self._args[0]
		else:
			quantity = int(self._args[0])
			name = self._args[1]

		#~ Item the player want to take
		i = item.model.loadBy({'name': name}, ['id_item'])

		if len(i) == 0:
			raise item.exception(_('ERROR_TAKE_UNKNOWN_ITEM'))

		i = str(i[0]['id_item'])
		#~ Available items in the area
		items = area.area.getItems(self._player.getAreaId())

		if i not in items.keys():
			raise item.exception(_('ERROR_TAKE_ITEM_NOT_AVAILABLE'))

		if quantity > items[i]['quantity']:
			raise item.exception(_('ERROR_TAKE_QUANTITY_TOO_HIGH'))

		i = [int(i)] * quantity
		self._player.addItemsToInventory(i)
		area.area.removeItems(self._player.getAreaId(), i)

		print(_('TAKE_CONFIRMATION_%(quantity)s_%(name)s') % {'quantity': quantity, 'name': name})

	def render(self, data):
		pass
