# -*- coding: utf-8 -*-

from models import area, creature
import core.command
from core.fight import fight
from core.localisation import _
from random import randint

class move(core.command.command):
	"""
	Move command
	"""

	def run(self):
		"""
		c.run()

		Move the player in the desired direction.
		"""
		if len(self._args) == 0:
			raise core.command.exception(_('ERROR_MOVE_NO_DIRECTION_GIVEN'))

		direction = self._args[0]
		if direction not in area.area.getDirections():
			raise core.command.exception(_('ERROR_MOVE_INVALID_DIRECTION_%s') % direction)
		curAreaId = self._player.getAreaId()
		curArea = area.model.loadById(curAreaId)

		ret = {'direction': direction}

		a = area.area.getNeighbourFromDirection(curAreaId, direction)

		if area.area.canGoTo(curArea['directions'], direction) is False or a is None:
			raise core.command.exception(_('ERROR_MOVE_DIRECTION_NOT_AVAILABLE'))
		else:
			wasFighting = self._player.isFighting()
			f = fight.getFight()
			if wasFighting:
				enemy = f.enemy

				if not fight.canFlee(self._player._model, enemy):
					raise core.fight.exception(_('ERROR_FLEE_FIGHT_FAILS'))
				else:
					fight.stopFight()
					ret['flee'] = True
					ret['enemy'] = enemy['name']

			self._player.goTo(a._model['id_area'])

			# let's be fair, if the player succesfully ran away from a
			# fight, he probably does not want to arrive right away in a
			# new one
			enemy = None
			if not wasFighting:
				probability = randint(0, 1000) / 1000.0
				enemy = creature.creature.getFromAreaType(
					a._model['id_area_type'],
					probability
				)

			if enemy is not None:
				ret['enemy'] = enemy['name']
				f = fight.startFight(self._player, enemy)
				# Deal with enemy attacking first
				damages = f.enemyTriesToAttackFirst(self._player)
				if damages is not None:
					ret['damages'] = damages

		return ret

	def render(self, data):
		fleeConfirmMsg = _('MOVE_CONFIRMATION_{direction}_FIGHT_FLEE_{enemy}')
		moveConfirmFightMsg = _('MOVE_CONFIRMATION_{direction}_FIGHT_{enemy}')
		moveConfirmAmbush = _('MOVE_CONFIRMATION_{direction}_AMBUSH_{enemy}')
		attackConfirmEnemy = _('ATTACK_CONFIRM_ENEMY_TO_PLAYER_{enemy}_{damages}')
		ret = []
		if 'enemy' in data.keys():
			# Ran away from an enemy
			if 'flee' in data.keys():
				ret.append(fleeConfirmMsg)
			# arrived face to face with an enemy
			# The enemy has been faster than the player and attacked first
			elif 'damages' in data.keys():
				ret.append(moveConfirmAmbush)
				ret.append(attackConfirmEnemy)
			else:
				ret.append(moveConfirmFightMsg)

			return '\n'.join(ret).format(**data)
		else:
			return _('MOVE_CONFIRMATION_%s') % data['direction']
