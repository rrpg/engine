# -*- coding: utf-8 -*-

from models import item_container, item
from core.commands import item_interaction
import core.command
from core.localisation import _

class open(item_interaction.item_interaction):
	def run(self):
		"""
		c.run()

		Open an item container in the area where the player is.
		The result of the command is a list of the items of the container
		"""
		index = None
		if len(self._args) == 0:
			raise core.command.exception(_('ERROR_OPEN_NO_CONTAINER_PROVIDED'))

		index = None
		if len(self._args) == 2:
			index = self._args[1]

		container = self._getContainerFromIdAreaTypeAndIndex(
			self._player.getAreaId(),
			self._args[0],
			index
		)

		items = item.inventory.fromStr(container['items'])

		result = {'container_type': self._args[0], 'items': list()}
		for i in items:
			it = item.model.loadById(i)
			result['items'].append({
				'name': it['name'],
				'quantity': items[i]['quantity']
			})

		return result

	def render(self, data):
		output = list()
		output.append(_('ITEMS_IN_CONTAINER_%s') % data['container_type'])
		for i in data['items']:
			output.append(str(i['quantity']).rjust(3) + ' ' + i['name'])
		return '\n'.join(output)
