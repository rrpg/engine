# -*- coding: utf-8 -*-
import unittest
import sys
import os
sys.path.append(os.path.realpath(__file__ + "/../../../"))

import tests.common
from core.localisation import _
import json


class moveTests(tests.common.common):
	def test_no_direction_given_text(self):
		self.rpgText.setAction([_('MOVE_COMMAND')])
		output = self.rpgText._runAction()
		self.assertEquals(output, _('ERROR_MOVE_NO_DIRECTION_GIVEN'))

	def test_no_direction_given_json(self):
		self.rpgJSON.setAction([_('MOVE_COMMAND')])
		output = self.rpgJSON._runAction()
		self.assertEquals(output, {"error": {"message": _('ERROR_MOVE_NO_DIRECTION_GIVEN'), "code": 1}})

	def test_invalid_direction_text(self):
		self.rpgText.setAction([_('MOVE_COMMAND'), 'bad-direction'])
		output = self.rpgText._runAction()
		self.assertEquals(output, _('ERROR_MOVE_INVALID_DIRECTION_%s') % 'bad-direction')

	def test_invalid_direction_json(self):
		self.rpgJSON.setAction([_('MOVE_COMMAND'), 'bad-direction'])
		output = self.rpgJSON._runAction()
		self.assertEquals(output, {"error": {"message": _('ERROR_MOVE_INVALID_DIRECTION_%s') % 'bad-direction', "code": 1}})

	def test_not_available_direction_text(self):
		self.rpgText.setAction([_('MOVE_COMMAND'), _('DIRECTION_KEY_EAST')])
		output = self.rpgText._runAction()
		self.assertEquals(output, _('ERROR_MOVE_DIRECTION_NOT_AVAILABLE'))

	def test_not_available_direction_json(self):
		self.rpgJSON.setAction([_('MOVE_COMMAND'), _('DIRECTION_KEY_EAST')])
		output = self.rpgJSON._runAction()
		self.assertEquals(output, {"error": {"message": _('ERROR_MOVE_DIRECTION_NOT_AVAILABLE'), "code": 1}})

	def test_move_with_fight_start_text(self):
		self.rpgText.setAction([_('MOVE_COMMAND'), _('DIRECTION_KEY_SOUTH')])
		self.rpgText._runAction()
		self.rpgText.setAction([_('MOVE_COMMAND'), _('DIRECTION_KEY_EAST')])
		output = self.rpgText._runAction()
		formatData = {'direction': _('DIRECTION_KEY_EAST'), 'enemy': 'rat'}
		self.assertEquals(output, _('MOVE_CONFIRMATION_{direction}_FIGHT_{enemy}').format(**formatData))

	def test_move_with_fight_start_json(self):
		self.rpgJSON.setAction([_('MOVE_COMMAND'), _('DIRECTION_KEY_SOUTH')])
		self.rpgJSON._runAction()
		self.rpgJSON.setAction([_('MOVE_COMMAND'), _('DIRECTION_KEY_EAST')])
		output = self.rpgJSON._runAction()
		self.assertEquals(output, {'direction': _('DIRECTION_KEY_EAST'), 'enemy': 'rat'})

	def test_text(self):
		self.rpgText.setAction([_('MOVE_COMMAND'), _('DIRECTION_KEY_SOUTH')])
		output = self.rpgText._runAction()
		self.assertEquals(output, _('MOVE_CONFIRMATION_%s') % _('DIRECTION_KEY_SOUTH'))

	def test_json(self):
		self.rpgJSON.setAction([_('MOVE_COMMAND'), _('DIRECTION_KEY_SOUTH')])
		output = self.rpgJSON._runAction()
		self.assertEquals(output, {"direction": _('DIRECTION_KEY_SOUTH')})
