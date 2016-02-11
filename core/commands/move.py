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
			if self._player.isFighting():
				enemy = core.fight.getEnemy()
				if self._player._model['stat_speed'] < enemy['stat_speed']:
					raise core.fight.exception(_('ERROR_FLEE_FIGHT_FAILS'))
				else:
					core.fight.stopFight(self._player)
			self._player.goTo(a._model['id_area'])
			probability = randint(0, 1000) / 1000.0
			enemy = creature.creature.getFromAreaType(
				a._model['id_area_type'],
				probability
			)

			if enemy is not None:
				ret['enemy'] = enemy['name']
				core.fight.startFight(self._player, enemy)

		return ret

	def render(self, data):
		if 'enemy' in data.keys():
			return _('MOVE_CONFIRMATION_%(direction)s_FIGHT_%(enemy)s') % {
				'direction': data['direction'], 'enemy': data['enemy']
			}
		else:
			return _('MOVE_CONFIRMATION_%s') % data['direction']
