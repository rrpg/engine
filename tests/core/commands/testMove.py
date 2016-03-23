# -*- coding: utf-8 -*-
import unittest

import tests.common
from core.localisation import _
import json


class moveTests(tests.common.common):
	def test_no_direction_given_text(self):
		self.rpg.setAction([_('MOVE_COMMAND')])
		output = self.rpg._runAction()
		self.assertEquals(output, _('ERROR_MOVE_NO_DIRECTION_GIVEN'))

	def test_no_direction_given_json(self):
		self.rpg.setAction([_('MOVE_COMMAND')])
		output = self.rpg._runAction(True)
		self.assertEquals(output, {"error": {"message": _('ERROR_MOVE_NO_DIRECTION_GIVEN'), "code": 1}})

	def test_invalid_direction_text(self):
		self.rpg.setAction([_('MOVE_COMMAND'), 'bad-direction'])
		output = self.rpg._runAction()
		self.assertEquals(output, _('ERROR_MOVE_INVALID_DIRECTION_%s') % 'bad-direction')

	def test_invalid_direction_json(self):
		self.rpg.setAction([_('MOVE_COMMAND'), 'bad-direction'])
		output = self.rpg._runAction(True)
		self.assertEquals(output, {"error": {"message": _('ERROR_MOVE_INVALID_DIRECTION_%s') % 'bad-direction', "code": 1}})

	def test_not_available_direction_text(self):
		self.rpg.setAction([_('MOVE_COMMAND'), _('DIRECTION_KEY_EAST')])
		output = self.rpg._runAction()
		self.assertEquals(output, _('ERROR_MOVE_DIRECTION_NOT_AVAILABLE'))

	def test_not_available_direction_json(self):
		self.rpg.setAction([_('MOVE_COMMAND'), _('DIRECTION_KEY_EAST')])
		output = self.rpg._runAction(True)
		self.assertEquals(output, {"error": {"message": _('ERROR_MOVE_DIRECTION_NOT_AVAILABLE'), "code": 1}})

	def test_move_with_fight_start_text(self):
		self.rpg.setAction([_('MOVE_COMMAND'), _('DIRECTION_KEY_SOUTH')])
		self.rpg._runAction()
		self.rpg.setAction([_('MOVE_COMMAND'), _('DIRECTION_KEY_EAST')])
		output = self.rpg._runAction()
		formatData = {'direction': _('DIRECTION_KEY_EAST'), 'enemy': 'rat'}
		self.assertEquals(output, _('MOVE_CONFIRMATION_{direction}_FIGHT_{enemy}').format(**formatData))

	def test_move_with_fight_start_json(self):
		self.rpg.setAction([_('MOVE_COMMAND'), _('DIRECTION_KEY_SOUTH')])
		self.rpg._runAction(True)
		self.rpg.setAction([_('MOVE_COMMAND'), _('DIRECTION_KEY_EAST')])
		output = self.rpg._runAction(True)
		self.assertEquals(output, {'direction': _('DIRECTION_KEY_EAST'), 'enemy': 'rat', 'x': 1, 'y': 0})

	def test_move_flee_fight_text(self):
		self.rpg.setAction([_('MOVE_COMMAND'), _('DIRECTION_KEY_SOUTH')])
		self.rpg._runAction()
		self.rpg.setAction([_('MOVE_COMMAND'), _('DIRECTION_KEY_EAST')])
		self.rpg._runAction()
		self.rpg.setAction([_('MOVE_COMMAND'), _('DIRECTION_KEY_WEST')])
		output = self.rpg._runAction()
		formatData = {'direction': _('DIRECTION_KEY_WEST'), 'enemy': 'rat'}
		self.assertEquals(output, _('MOVE_CONFIRMATION_{direction}_FIGHT_FLEE_{enemy}').format(**formatData))

	def test_move_flee_fight_json(self):
		self.rpg.setAction([_('MOVE_COMMAND'), _('DIRECTION_KEY_SOUTH')])
		self.rpg._runAction(True)
		self.rpg.setAction([_('MOVE_COMMAND'), _('DIRECTION_KEY_EAST')])
		self.rpg._runAction(True)
		self.rpg.setAction([_('MOVE_COMMAND'), _('DIRECTION_KEY_WEST')])
		output = self.rpg._runAction(True)
		self.assertEquals(output, {'direction': _('DIRECTION_KEY_WEST'), 'enemy': 'rat', 'flee': True, 'x': 0, 'y': 0})

	def test_move_noflee_fight_text(self):
		self.rpg.setAction([_('MOVE_COMMAND'), _('DIRECTION_KEY_SOUTH')])
		self.rpg._runAction()
		self.rpg.setAction([_('MOVE_COMMAND'), _('DIRECTION_KEY_WEST')])
		self.rpg._runAction()
		self.rpg.setAction([_('MOVE_COMMAND'), _('DIRECTION_KEY_EAST')])
		output = self.rpg._runAction()
		formatData = {'direction': _('DIRECTION_KEY_WEST'), 'enemy': 'rat'}
		self.assertEquals(output, _('ERROR_FLEE_FIGHT_FAILS'))

	def test_move_noflee_fight_json(self):
		self.rpg.setAction([_('MOVE_COMMAND'), _('DIRECTION_KEY_SOUTH')])
		self.rpg._runAction(True)
		self.rpg.setAction([_('MOVE_COMMAND'), _('DIRECTION_KEY_WEST')])
		self.rpg._runAction(True)
		self.rpg.setAction([_('MOVE_COMMAND'), _('DIRECTION_KEY_EAST')])
		output = self.rpg._runAction(True)
		self.assertEquals(output, {"error": {"message": _('ERROR_FLEE_FIGHT_FAILS'), "code": 1}})

	def test_text(self):
		self.rpg.setAction([_('MOVE_COMMAND'), _('DIRECTION_KEY_SOUTH')])
		output = self.rpg._runAction()
		self.assertEquals(output, _('MOVE_CONFIRMATION_%s') % _('DIRECTION_KEY_SOUTH'))

	def test_json(self):
		self.rpg.setAction([_('MOVE_COMMAND'), _('DIRECTION_KEY_SOUTH')])
		output = self.rpg._runAction(True)
		self.assertEquals(output, {"direction": _('DIRECTION_KEY_SOUTH'), 'x': 0, 'y': 0})
