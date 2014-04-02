# -*- coding: utf-8 -*-

from models import place
import core.command
from core.localisation import _


class enter(core.command.command):
	"""
	Enter command
	"""

	def run(self):
		"""
		c.run()

		With this command, the player can enter places such as houses, shops,
		dungeons...
		"""
		if len(self._args) == 0:
			raise core.command.exception(_('ERROR_ENTER_NO_PLACE_GIVEN'))

		areaType = self._args[0]

		p = place.factory.getFromEntranceArea(self._player.getAreaId(), areaType)
		if p is None:
			raise place.exception(_('ERROR_ENTER_PLACE_NOT_AVAILABLE'))
			return

		if p['entrance_id'] is None:
			p = place.factory.generate(p, areaType)
		self._player.goTo(p['entrance_id'])
		return [_('ENTER_CONFIRMATION')]

	def render(self, data):
		return data[0]
