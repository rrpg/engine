# -*- coding: utf-8 -*-
import unittest
import sys
import os
sys.path.append(os.path.realpath(__file__ + "/../../../"))

import tests.common
from tests.output_capturer import capturer
from core.localisation import _
import json


class moveTests(tests.common.common):
	def test_no_direction_given_text(self):
		with capturer() as output:
			self.rpgText.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', [_('MOVE_COMMAND')])
			self.rpgText._runAction()
		self.assertTrue(output == [_('ERROR_MOVE_NO_DIRECTION_GIVEN')])

	def test_no_direction_given_json(self):
		with capturer() as output:
			self.rpgJSON.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', [_('MOVE_COMMAND')])
			self.rpgJSON._runAction()
		self.assertTrue(json.loads(output[0]) == {"error": {"message": _('ERROR_MOVE_NO_DIRECTION_GIVEN'), "code": 1}})

	def test_invalid_direction_text(self):
		with capturer() as output:
			self.rpgText.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', [_('MOVE_COMMAND'), 'bad-direction'])
			self.rpgText._runAction()
		self.assertTrue(output == [_('ERROR_MOVE_INVALID_DIRECTION_%s') % 'bad-direction'])

	def test_invalid_direction_json(self):
		with capturer() as output:
			self.rpgJSON.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', [_('MOVE_COMMAND'), 'bad-direction'])
			self.rpgJSON._runAction()
		self.assertTrue(json.loads(output[0]) == {"error": {"message": _('ERROR_MOVE_INVALID_DIRECTION_%s') % 'bad-direction', "code": 1}})

	def test_not_available_direction_text(self):
		with capturer() as output:
			self.rpgText.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', [_('MOVE_COMMAND'), _('DIRECTION_KEY_EAST')])
			self.rpgText._runAction()
		self.assertTrue(output == [_('ERROR_MOVE_DIRECTION_NOT_AVAILABLE')])

	def test_not_available_direction_json(self):
		with capturer() as output:
			self.rpgJSON.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', [_('MOVE_COMMAND'), _('DIRECTION_KEY_EAST')])
			self.rpgJSON._runAction()
		self.assertTrue(json.loads(output[0]) == {"error": {"message": _('ERROR_MOVE_DIRECTION_NOT_AVAILABLE'), "code": 1}})

	def test_text(self):
		with capturer() as output:
			self.rpgText.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', [_('MOVE_COMMAND'), _('DIRECTION_KEY_NORTH')])
			self.rpgText._runAction()
		self.assertTrue(output == [_('MOVE_CONFIRMATION_%s') % _('DIRECTION_KEY_NORTH')])

	def test_json(self):
		with capturer() as output:
			self.rpgJSON.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', [_('MOVE_COMMAND'), _('DIRECTION_KEY_NORTH')])
			self.rpgJSON._runAction()
		self.assertTrue(json.loads(output[0]) == {"direction": _('DIRECTION_KEY_NORTH')})

unittest.main()
