# -*- coding: utf-8 -*-

from models import item_container, item, area
from core.commands import item_interaction
import core.command
from core.localisation import _


class take(item_interaction.item_interaction):
	def run(self):
		try:
			(quantity, name, containerType, containerIndex) = self._getArgs()
		except item_interaction.exception as e:
			if e.code is item_interaction.exception.CODE_NO_ITEM_GIVEN:
				raise core.command.exception(_('ERROR_TAKE_NO_ITEM_GIVEN'))
			elif e.code is item_interaction.exception.CODE_INVALID_QUANTITY:
				raise core.command.exception(_('ERROR_TAKE_INVALID_QUANTITY'))

		# Item the player want to take
		i = item.model.loadBy({'name': name}, ['id_item'])

		if len(i) == 0:
			raise item.exception(_('ERROR_TAKE_UNKNOWN_ITEM'))
		i = str(i[0]['id_item'])

		if containerType is None:
			# Available items in the area
			items = area.area.getItems(self._player.getAreaId())
		else:
			# Item to be taken in a container
			container = item_container.factory.getFromIdAreaTypeAndIndex(
				self._player.getAreaId(),
				containerType,
				containerIndex
			)
			items = item.inventory.fromStr(container['items'])

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
