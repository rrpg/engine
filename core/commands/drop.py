# -*- coding: utf-8 -*-

from models import item_container, item, area
from core.commands import item_interaction
import core.command
from core.localisation import _

class drop(item_interaction.item_interaction):
	def run(self):
		"""
		c.run()

		Drop an item being in the inventory. The item will be let on the floor
		of the player's current area.
		"""
		try:
			(quantity, name, containerType, containerIndex) = self._getArgs()
		except item_interaction.exception as e:
			if e.code is item_interaction.exception.CODE_NO_ITEM_GIVEN:
				raise core.command.exception(_('ERROR_DROP_NO_ITEM_GIVEN'))
			elif e.code is item_interaction.exception.CODE_TOO_LOW_QUANTITY:
				raise core.command.exception(_('ERROR_DROP_TOO_LOW_QUANTITY'))
			elif e.code is item_interaction.exception.CODE_INVALID_FORMAT_QUANTITY:
				raise core.command.exception(_('ERROR_DROP_INVALID_FORMAT_QUANTITY'))
			elif e.code is item_interaction.exception.CODE_INVALID_CONTAINER_INDEX:
				raise core.command.exception(_('ERROR_DROP_INVALID_CONTAINER_INDEX'))

		if containerType is not None:
			# Item to be taken in a container
			container = self._getContainerFromIdAreaTypeAndIndex(
				self._player.getAreaId(),
				containerType,
				containerIndex
			)

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
		i = [int(i)] * quantity
		self._player.removeItemsFromInventory(i)

		if containerType is None:
			area.area.addItems(self._player.getAreaId(), i)
		else:
			item_container.container.addItems(container, i)


		return {'quantity': quantity, 'name': name}

	def render(self, data):
		return _('DROP_CONFIRMATION_%(quantity)s_%(name)s') % data
