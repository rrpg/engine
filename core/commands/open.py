# -*- coding: utf-8 -*-

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

		return []

	def render(self, data):
		return ''
