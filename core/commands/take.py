# -*- coding: utf-8 -*-

from models import item, area
import core.command
from core.localisation import _


class take(core.command.command):
	def run(self):
		(quantity, name, container, containerIndex) = self._getArgs()

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

	def _getArgs(self):
		nbArgs = len(self._args)
		self._args.reverse()

		container = None
		containerIndex = 1
		argsNames = ['containerId', 'container', 'name']
		args = {'name': '', 'container': None, 'containerId': 1}

		if nbArgs == 0:
			raise core.command.exception(_('ERROR_TAKE_NO_ITEM_GIVEN'))

		try:
			quantity = int(self._args[nbArgs - 1])
			self._args.pop()
		except ValueError:
			# 4 arguments have been provided, but the quantity is invalid
			if nbArgs == 4:
				raise core.command.exception(_('ERROR_TAKE_INVALID_QUANTITY'))
			quantity = 1

		while len(self._args) > 0:
			args[argsNames.pop()] = self._args.pop()

		return (quantity, args['name'], args['container'], args['containerId'])
