# -*- coding: utf-8 -*-
import unittest
try: # pragma: no cover
	import mock
except ImportError: # pragma: no cover
	import unittest.mock as mock

import tests.common
import core
from core.localisation import _
from core import Rpg
import models.settings
import json
import sqlite3

def randintMock(minVal, maxVal):
	return maxVal

def randintMock_Big(minVal, maxVal):
	return maxVal * 15


class attackTests(tests.common.common):
	def move_to_attack(self, engine):
		engine.setAction([_('MOVE_COMMAND'), _('DIRECTION_KEY_SOUTH')])
		engine._runAction()
		engine.setAction([_('MOVE_COMMAND'), _('DIRECTION_KEY_EAST')])
		engine._runAction()

	def move_to_big_rat_attack(self, engine):
		engine.setAction([_('MOVE_COMMAND'), _('DIRECTION_KEY_SOUTH')])
		engine._runAction()
		engine.setAction([_('MOVE_COMMAND'), _('DIRECTION_KEY_WEST')])
		engine._runAction()

	def test_not_fighting_text(self):
		self.rpg.setAction([_('ATTACK_COMMAND')])
		output = self.rpg._runAction()
		self.assertEquals(output, _('ERROR_FIGHT_NOT_FIGHTING'))

	def test_not_fighting_json(self):
		self.rpg.setAction([_('ATTACK_COMMAND')])
		output = self.rpg._runAction(True)
		self.assertEquals(output,  {'error': {'message': _('ERROR_FIGHT_NOT_FIGHTING'), 'code': 1}})

	@mock.patch('random.randint', side_effect=randintMock)
	def test_attack_text(self, randintMockFun):
		self.move_to_attack(self.rpg)
		self.rpg.setAction([_('ATTACK_COMMAND')])
		output = self.rpg._runAction()
		# The player deals 2 damage points because of 4 attack - 2 defence
		# The rat deals 0 damage points because of 2 attack - 2 defence
		expected = '\n'.join([
			_('ATTACK_CONFIRM_PLAYER_TO_ENEMY_{enemy}_{damages}').format(**{'enemy': 'rat', 'damages': 2}),
			_('ATTACK_CONFIRM_ENEMY_TO_PLAYER_{enemy}_{damages}').format(**{'enemy': 'rat', 'damages': 0})
		])
		self.assertEquals(output, expected)

	@mock.patch('random.randint', side_effect=randintMock)
	def test_attack_json(self, randintMockFun):
		self.move_to_attack(self.rpg)
		self.rpg.setAction([_('ATTACK_COMMAND')])
		output = self.rpg._runAction(True)
		# The player deals 2 damage points because of 4 attack - 2 defence
		# The rat deals 0 damage points because of 2 attack - 2 defence
		expected = {
			'enemy': {
				'name': 'rat',
				'stat_defence': 2,
				'stat_attack': 2,
				'stat_max_hp': 15,
				'stat_current_hp': 13,
				'stat_speed': 1,
				'stat_luck': 25
			},
			'attackResult': {
				'damagesToPlayer': 0,
				'winner': None,
				'damagesToEnemy': 2,
				'fightFinished': False
			}
		}
		self.assertEquals(output, expected)

	@mock.patch('random.randint', side_effect=randintMock_Big)
	def test_attack_kill_enemy_text(self, randintMockFun):
		self.move_to_attack(self.rpg)
		self.rpg.setAction([_('ATTACK_COMMAND')])
		output = self.rpg._runAction()
		# The player deals 30 damage points because of (4 attack - 2 defence) * 15 from the mock
		# The rat deals 0 damage points because of (2 attack - 2 defence) * 15 from the mock
		expected = '\n'.join([
			_('ATTACK_CONFIRM_PLAYER_TO_ENEMY_{enemy}_{damages}').format(**{'enemy': 'rat', 'damages': 30}),
			_('ATTACK_VICTORY_{enemy}').format(**{'enemy': 'rat'})
		])
		self.assertEquals(output, expected)

	@mock.patch('random.randint', side_effect=randintMock_Big)
	def test_attack_kill_enemy_json(self, randintMockFun):
		self.move_to_attack(self.rpg)
		self.rpg.setAction([_('ATTACK_COMMAND')])
		output = self.rpg._runAction(True)
		# The player deals 30 damage points because of (4 attack - 2 defence) * 15 from the mock
		# The rat deals 0 damage points because of (2 attack - 2 defence) * 15 from the mock
		expected = {
			'enemy': {
				'name': 'rat',
				'stat_defence': 2,
				'stat_attack': 2,
				'stat_max_hp': 15,
				'stat_current_hp': 0,
				'stat_speed': 1,
				'stat_luck': 25
			},
			'attackResult': {
				'damagesToPlayer': None,
				'winner': self.rpg._player,
				'damagesToEnemy': 30,
				'fightFinished': True
			}
		}
		self.assertEquals(output, expected)

	@mock.patch('random.randint', side_effect=randintMock_Big)
	def test_attack_kill_player_text(self, randintMockFun):
		self.move_to_big_rat_attack(self.rpg)
		self.assertFalse(self.rpg.isGameOver())
		self.rpg.setAction([_('ATTACK_COMMAND')])
		output = self.rpg._runAction()
		self.assertTrue(self.rpg.isGameOver())
		# The player deals 30 damage points because of (4 attack - 2 defence) * 15 from mock
		# The rat deals 30 damage points because of (4 attack - 2 defence) * 15 from mock
		# The giant rat kills the player
		expected = '\n'.join([
			_('ATTACK_CONFIRM_PLAYER_TO_ENEMY_{enemy}_{damages}').format(**{'enemy': 'giant rat', 'damages': 30}),
			_('ATTACK_CONFIRM_ENEMY_TO_PLAYER_{enemy}_{damages}').format(**{'enemy': 'giant rat', 'damages': 30}),
			_('ATTACK_LOST_{enemy}').format(**{'enemy': 'giant rat'})
		])
		self.assertEquals(output, expected)

	@mock.patch('random.randint', side_effect=randintMock_Big)
	def test_attack_kill_player_json(self, randintMockFun):
		self.move_to_big_rat_attack(self.rpg)
		self.rpg.setAction([_('ATTACK_COMMAND')])
		output = self.rpg._runAction(True)
		# The player deals 30 damage points because of (4 attack - 2 defence) * 15 from mock
		# The rat deals 30 damage points because of (4 attack - 2 defence) * 15 from mock
		# The giant rat kills the player
		expected = {
			'enemy': {
				'name': 'giant rat',
				'stat_defence': 2,
				'stat_attack': 4,
				'stat_max_hp': 35,
				'stat_current_hp': 5,
				'stat_speed': 2,
				'stat_luck': 25
			},
			'attackResult': {
				'damagesToPlayer': 30,
				'winner': {
					'name': 'giant rat',
					'stat_defence': 2,
					'stat_attack': 4,
					'stat_max_hp': 35,
					'stat_current_hp': 5,
					'stat_speed': 2,
					'stat_luck': 25
				},
				'damagesToEnemy': 30,
				'fightFinished': True
			}
		}
		self.assertEquals(output, expected)

