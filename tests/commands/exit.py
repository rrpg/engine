# -*- coding: utf-8 -*-
import unittest
import sys
import os
sys.path.append(os.path.realpath(__file__ + "/../../../"))

import tests.common
from tests.output_capturer import capturer
from core.localisation import _
import json

class exitTests(tests.common.common):
	def test_no_place_given_text(self):
		self.rpgText.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', [_('EXIT_COMMAND')])
		output = self.rpgText._runAction()
		self.assertTrue(output == _('ERROR_EXIT_NO_PLACE_GIVEN'))

	def test_no_place_given_json(self):
		self.rpgJSON.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', [_('EXIT_COMMAND')])
		output = self.rpgJSON._runAction()
		self.assertTrue(output == {"error": {"message": _('ERROR_EXIT_NO_PLACE_GIVEN'), "code": 1}})

	def test_place_not_available_text(self):
		self.rpgText.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', [_('EXIT_COMMAND'), _('PLACE_TYPE_CAVE')])
		output = self.rpgText._runAction()
		self.assertTrue(output == _('ERROR_ENTER_PLACE_NOT_AVAILABLE'))

	def test_no_place_given_json(self):
		self.rpgJSON.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', [_('EXIT_COMMAND'), _('PLACE_TYPE_CAVE')])
		output = self.rpgJSON._runAction()
		self.assertTrue(output == {"error": {"message": _('ERROR_ENTER_PLACE_NOT_AVAILABLE'), "code": 1}})

	def test_wrong_place_text(self):
		self.rpgText.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', [_('EXIT_COMMAND'), 'dummyplace'])
		output = self.rpgText._runAction()
		self.assertTrue(output == _('ERROR_UNKNOWN_PLACE_TYPE'))

	def test_wrong_place_given_json(self):
		self.rpgJSON.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', [_('EXIT_COMMAND'), 'dummyplace'])
		output = self.rpgJSON._runAction()
		self.assertTrue(output == {"error": {"message": _('ERROR_UNKNOWN_PLACE_TYPE'), "code": 1}})

	def test_when_still_out_text(self):
		self.rpgText.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', [_('EXIT_COMMAND'), _('PLACE_TYPE_DUNGEON')])
		output = self.rpgText._runAction()
		self.assertTrue(output == _('ERROR_ENTER_PLACE_NOT_AVAILABLE'))

	def test_when_still_out_json(self):
		self.rpgJSON.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', [_('EXIT_COMMAND'), _('PLACE_TYPE_DUNGEON')])
		output = self.rpgJSON._runAction()
		self.assertTrue(output == {"error": {"message": _('ERROR_ENTER_PLACE_NOT_AVAILABLE'), "code": 1}})

	def test_text(self):
		self.rpgText.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', [_('ENTER_COMMAND'), _('PLACE_TYPE_DUNGEON')])
		self.rpgText._runAction()
		self.rpgText.setAction([_('EXIT_COMMAND'), _('PLACE_TYPE_DUNGEON')])
		output = self.rpgText._runAction()
		self.assertTrue(output == _('EXIT_CONFIRMATION'))

	def test_json(self):
		self.rpgJSON.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', [_('ENTER_COMMAND'), _('PLACE_TYPE_DUNGEON')])
		self.rpgJSON._runAction()
		self.rpgJSON.setAction([_('EXIT_COMMAND'), _('PLACE_TYPE_DUNGEON')])
		output = self.rpgJSON._runAction()
		self.assertTrue(output == [_('EXIT_CONFIRMATION')])

unittest.main()
