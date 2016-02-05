# -*- coding: utf-8 -*-

import core.command
from core.localisation import _

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
		self._player.saveProgress()
		return {'saved': True}

	def render(self, data):
		if data['saved']:
			return _('SAVE_CONFIRMATION_OK')
		else:
			return _('SAVE_CONFIRMATION_KO')
