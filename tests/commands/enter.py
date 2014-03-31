# -*- coding: utf-8 -*-
import unittest
import sys
import os
sys.path.append(os.path.realpath(__file__ + "/../../../"))

import tests.common
from tests.output_capturer import capturer
from core.localisation import _


class enterTests(tests.common.common):
	def test_no_place_given_text(self):
		with capturer() as output:
			self.rpgText.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', [_('ENTER_COMMAND')])
			self.rpgText._runAction()
		self.assertTrue(output == [_('ERROR_ENTER_NO_PLACE_GIVEN')])

	def test_no_place_given_json(self):
		with capturer() as output:
			self.rpgJSON.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', [_('ENTER_COMMAND')])
			self.rpgJSON._runAction()
		self.assertTrue(output == ['{"error": {"message": "' + _('ERROR_ENTER_NO_PLACE_GIVEN') + '", "code": 1}}'])

	def test_place_not_available_text(self):
		with capturer() as output:
			self.rpgText.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', [_('ENTER_COMMAND'), _('PLACE_TYPE_CAVE')])
			self.rpgText._runAction()
		self.assertTrue(output == [_('ERROR_ENTER_PLACE_NOT_AVAILABLE')])

	def test_no_place_given_json(self):
		with capturer() as output:
			self.rpgJSON.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', [_('ENTER_COMMAND'), 'cave'])
			self.rpgJSON._runAction()
		self.assertTrue(output == ['{"error": {"message": "' + _('ERROR_ENTER_PLACE_NOT_AVAILABLE') + '", "code": 1}}'])

	def test_wrong_place_text(self):
		with capturer() as output:
			self.rpgText.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', [_('ENTER_COMMAND'), 'dummyplace'])
			self.rpgText._runAction()
		self.assertTrue(output == [_('ERROR_UNKNOWN_PLACE_TYPE')])

	def test_wrong_place_given_json(self):
		with capturer() as output:
			self.rpgJSON.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', [_('ENTER_COMMAND'), 'dummyplace'])
			self.rpgJSON._runAction()
		self.assertTrue(output == ['{"error": {"message": "' + _('ERROR_UNKNOWN_PLACE_TYPE') + '", "code": 1}}'])

	def test_when_already_in_text(self):
		self.rpgText.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', [_('ENTER_COMMAND'), _('PLACE_TYPE_DUNGEON')])
		with capturer() as output:
			self.rpgText._runAction()
		self.rpgText.setAction([_('ENTER_COMMAND'), _('PLACE_TYPE_DUNGEON')])
		with capturer() as output:
			self.rpgText._runAction()
		self.assertTrue(output == [_('ERROR_ENTER_PLACE_NOT_AVAILABLE')])

	def test_when_already_in_json(self):
		self.rpgJSON.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', [_('ENTER_COMMAND'), _('PLACE_TYPE_DUNGEON')])
		with capturer() as output:
			self.rpgJSON._runAction()
		self.rpgJSON.setAction([_('ENTER_COMMAND'), _('PLACE_TYPE_DUNGEON')])
		with capturer() as output:
			self.rpgJSON._runAction()
		self.assertTrue(output == ['{"error": {"message": "' + _('ERROR_ENTER_PLACE_NOT_AVAILABLE') + '", "code": 1}}'])

	def test_text(self):
		with capturer() as output:
			self.rpgText.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', [_('ENTER_COMMAND'), _('PLACE_TYPE_DUNGEON')])
			self.rpgText._runAction()
		self.assertTrue(output == [_('ENTER_CONFIRMATION')])

	def test_json(self):
		with capturer() as output:
			self.rpgJSON.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', [_('ENTER_COMMAND'), _('PLACE_TYPE_DUNGEON')])
			self.rpgJSON._runAction()
		self.assertTrue(output == ['["' + _('ENTER_CONFIRMATION') + '"]'])

unittest.main()
