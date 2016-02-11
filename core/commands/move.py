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

		a = area.area.getNeighbourFromDirection(curAreaId, direction)

		if area.area.canGoTo(curArea['directions'], direction) is False or a is None:
			raise core.command.exception(_('ERROR_MOVE_DIRECTION_NOT_AVAILABLE'))
		else:
			self._player.goTo(a._model['id_area'])
			probability = randint(0, 1000) / 1000.0
			enemy = creature.creature.getFromAreaType(
				a._model['id_area_type'],
				probability
			)

			if enemy is not None:
				core.fight.startFight(self._player, enemy)

		return {'direction': direction}

	def render(self, data):
		return _('MOVE_CONFIRMATION_%s') % data['direction']
