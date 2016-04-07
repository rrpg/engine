# -*- coding: utf-8 -*-

import core.command
from core.localisation import _
from models.area import area
from models.saved_game import saved_game
from models.item_container import container


class save(core.command.command):
	"""
	Save command

	To save the game's progress
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
		saved_game.updateSavedGame(
			self._savedGameId,
			{'snapshot_player': self._player.getSnapshot()}
		)
		area.saveChangedAreas()
		container.saveChangedContainers()

	def render(self, data):
		return _('SAVE_CONFIRMATION_OK')
