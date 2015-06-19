# -*- coding: utf-8 -*-

from models import character, sentence
import random
import core.command
from core.localisation import _

class attack(core.command.command):
	"""
	Fight command
	"""

	def run(self):
		"""
		Attack someone in the same area
		"""
		if len(self._args) == 0:
			raise core.command.exception(_('ERROR_FIGHT_NO_TARGET_GIVEN'))

		targetName = self._args[0]

		return {'name': targetName}

	def render(self, data):
		return 'You attack ' + data['name']
