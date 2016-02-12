# -*- coding: utf-8 -*-

from models import area, creature
import core.command
import core.fight
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
			wasFighting = False
			if self._player.isFighting():
				enemy = core.fight.getEnemy()
				if self._player._model['stat_speed'] < enemy['stat_speed']:
					raise core.fight.exception(_('ERROR_FLEE_FIGHT_FAILS'))
				else:
					core.fight.stopFight(self._player)
					wasFighting = True
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
				core.fight.startFight(self._player, enemy)
				# Deal with enemy attacking first
				damages = core.fight.enemyTriesToAttackFirst(self._player)
				if damages is not None:
					ret['damages'] = damages

		return ret

	def render(self, data):
		ret = ''
		if 'enemy' in data.keys():
			# Ran away from an enemy
			if 'flee' in data.keys():
				ret = _('MOVE_CONFIRMATION_%(direction)s_FIGHT_FLEE_%(enemy)s')
			# arrived face to face with an enemy
			# The enemy has been faster than the player and attacked first
			elif 'damages' in data.keys():
				ret = _('MOVE_CONFIRMATION_%(direction)s_AMBUSH_%(enemy)s')
				ret += _('FIGHT_ENEMY_DAMAGES_%(enemy)s_%(damages)s')
			else:
				ret = _('MOVE_CONFIRMATION_%(direction)s_FIGHT_%(enemy)s')

			return ret % data
		else:
			return _('MOVE_CONFIRMATION_%s') % data['direction']
