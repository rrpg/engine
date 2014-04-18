# -*- coding: utf-8 -*-

from models import item_container, item
import core.command
from core.localisation import _

class open(core.command.command):
	def run(self):
		"""
		c.run()

		Open an item container in the area where the player is.
		The result of the command is a list of the items of the container
		"""
		if len(self._args) == 0:
			raise core.command.exception(_('ERROR_OPEN_NO_CONTAINER_PROVIDED'))

		containers = item_container.factory.getAllFromIdAreaAndType(
			self._player.getAreaId(),
			self._args[0]
		)

		if len(containers) > 1:
			raise core.command.exception(_('ERROR_OPEN_MULTIPLE_CONTAINERS_AVAILABLE'))

		items = item.inventory.fromStr(containers[0]['items'])

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
