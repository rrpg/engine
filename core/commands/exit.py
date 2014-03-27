# -*- coding: utf-8 -*-

from models import place
import core.command
from core.localisation import _


class exit(core.command.command):
	"""
	Exit command, to exit a place
	"""

	def run(self):
		"""
		c.run()

		With this command, the player can exit places such as houses, shops,
		dungeons... to go back in the world
		"""
		if len(self._args) == 0:
			raise core.command.exception(_('ERROR_EXIT_NO_PLACE_GIVEN'))

		areaType = self._args[0]

		p = place.factory.getFromExitArea(self._player.getAreaId(), areaType)
		if p is None:
			raise place.exception(_('ERROR_ENTER_PLACE_NOT_AVAILABLE'))
			return

		self._player.goTo(p['id_area'])
		return [_('EXIT_CONFIRMATION')]

	def render(self, data):
		print(data[0])
