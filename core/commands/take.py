# -*- coding: utf-8 -*-

from models import item, area
import core.command
from core.localisation import _


class take(core.command.command):
	def run(self):
		nbArgs = len(self._args)

		quantity = 1
		container = None
		containerIndex = 1
		#@TODO To refactor
		if nbArgs == 0:
			raise core.command.exception(_('ERROR_TAKE_NO_ITEM_GIVEN'))
		elif nbArgs == 1:
			name = self._args[0]
		elif nbArgs == 2:
			try:
				quantity = int(self._args[0])
				name = self._args[1]
			except ValueError:
				name = self._args[0]
				container = self._args[1]
		elif nbArgs == 3:
			try:
				quantity = int(self._args[0])
				name = self._args[1]
				container = self._args[2]
			except ValueError:
				name = self._args[0]
				container = self._args[1]
				try:
					containerIndex = int(self._args[2])
				except ValueError:
					raise core.command.exception(_('ERROR_TAKE_INVALID_CONTAINER_INDEX'))
		elif nbArgs == 4:
			try:
				quantity = int(self._args[0])
			except ValueError:
				raise core.command.exception(_('ERROR_TAKE_INVALID_QUANTITY'))
			name = self._args[1]
			container = self._args[2]
			try:
				containerIndex = int(self._args[3])
			except ValueError:
				raise core.command.exception(_('ERROR_TAKE_INVALID_CONTAINER_INDEX'))

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

		return {'quantity': quantity, 'name': name}

	def render(self, data):
		return _('TAKE_CONFIRMATION_%(quantity)s_%(name)s') % data
