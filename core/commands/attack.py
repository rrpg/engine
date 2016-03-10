# -*- coding: utf-8 -*-

import core.command
import core.fight
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
		enemy = core.fight.getEnemy()
		attackResult = core.fight.attack(
			self._player, enemy
		)

		return {
			'enemy': enemy,
			'attackResult': attackResult
		}

	def render(self, data):
		output = ['You attack ' + data['enemy']['name'] + ' and deal ' + str(data['attackResult']['damagesToEnemy']) + ' points of damage']

		if data['attackResult']['fightFinished']:
			output.append('The fight is over')

		return '\n'.join(output)
