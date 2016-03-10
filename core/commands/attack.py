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
		enemy = core.fight.getEnemy()

		if enemy is None:
			raise core.command.exception(_('ERROR_FIGHT_NOT_FIGHTING'))

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
