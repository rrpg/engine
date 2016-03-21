# -*- coding: utf-8 -*-

import core.command
from core.localisation import _
from models.area import area
from models.item_container import container


class save(core.command.command):
	"""
	Save command

	To save the game's progress, usable only in interactive mode
	"""

	def run(self):
		"""
		c.run()

		Saves the game's progress
		"""
		canSave = area.hasSavePoint(self._player.getAreaId())
		if not canSave:
			raise core.command.exception(_('ERROR_SAVE_NO_SAVE_POINT'))

		self._player.saveProgress()
		area.saveChangedAreas()
		container.saveChangedContainers()

	def render(self, data):
		return _('SAVE_CONFIRMATION_OK')
