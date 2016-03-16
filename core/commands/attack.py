# -*- coding: utf-8 -*-

import core.command
from core.fight import fight
from core.localisation import _

class attack(core.command.command):
	"""
	Fight command
	"""

	def run(self):
		"""
		Attack someone in the same area
		"""
		f = fight.getFight()

		if f is None:
			raise core.command.exception(_('ERROR_FIGHT_NOT_FIGHTING'))

		enemy = f.getEnemy()
		attackResult = f.attack()

		return {
			'enemy': enemy,
			'attackResult': attackResult
		}

	def render(self, data):
		attackConfirm = _('ATTACK_CONFIRM_PLAYER_TO_ENEMY_{enemy}_{damages}')
		attackConfirmEnemy = _('ATTACK_CONFIRM_ENEMY_TO_PLAYER_{enemy}_{damages}')
		attackVictory = _('ATTACK_VICTORY_{enemy}')
		attackLost = _('ATTACK_LOST_{enemy}')
		dataFormat = {
			'enemy': data['enemy']['name'],
			'damages': data['attackResult']['damagesToEnemy']
		}
		output = [attackConfirm.format(**dataFormat)]

		if data['attackResult']['damagesToPlayer'] is not None:
			dataFormat = {
				'enemy': data['enemy']['name'],
				'damages': data['attackResult']['damagesToPlayer']
			}
			output.append(attackConfirmEnemy.format(**dataFormat))


		if data['attackResult']['fightFinished']:
			dataFormat = {
				'enemy': data['enemy']['name']
			}
			if data['attackResult']['winner'] == self._player:
				output.append(attackVictory.format(**dataFormat))
			else:
				output.append(attackLost.format(**dataFormat))

		return '\n'.join(output)
