# -*- coding: utf-8 -*-
import unittest
import sys
import os
sys.path.append(os.path.realpath(__file__ + "/../../../"))

import tests.common
from core.localisation import _
import json


class takeTests(tests.common.common):
	def test_no_item_given_text(self):
		self.rpgText.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', [_('TAKE_COMMAND')])
		output = self.rpgText._runAction()
		self.assertTrue(output == _('ERROR_TAKE_NO_ITEM_GIVEN'))

	def test_no_item_given_json(self):
		self.rpgJSON.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', [_('TAKE_COMMAND')])
		output = self.rpgJSON._runAction()
		self.assertTrue(output == {"error": {"message": _('ERROR_TAKE_NO_ITEM_GIVEN'), "code": 1}})

	def test_unknown_item_text(self):
		self.rpgText.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', [_('TAKE_COMMAND'), 'some dummy item'])
		output = self.rpgText._runAction()
		self.assertTrue(output == _('ERROR_TAKE_UNKNOWN_ITEM'))

	def test_unknown_item_json(self):
		self.rpgJSON.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', [_('TAKE_COMMAND'), 'some dummy item'])
		output = self.rpgJSON._runAction()
		self.assertTrue(output == {"error": {"message": _('ERROR_TAKE_UNKNOWN_ITEM'), "code": 1}})

	def test_item_not_here_text(self):
		self.rpgText.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', [_('TAKE_COMMAND'), 'Mist potion'])
		output = self.rpgText._runAction()
		self.assertTrue(output == _('ERROR_TAKE_ITEM_NOT_AVAILABLE'))

	def test_item_not_here_json(self):
		self.rpgJSON.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', [_('TAKE_COMMAND'), 'Mist potion'])
		output = self.rpgJSON._runAction()
		self.assertTrue(output == {"error": {"message": _('ERROR_TAKE_ITEM_NOT_AVAILABLE'), "code": 1}})

	def test_quantity_too_high_text(self):
		self.rpgText.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', [_('TAKE_COMMAND'), 10, 'Heavy breastplate'])
		output = self.rpgText._runAction()
		self.assertTrue(output == _('ERROR_TAKE_QUANTITY_TOO_HIGH'))

	def test_quantity_too_high_json(self):
		self.rpgJSON.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', [_('TAKE_COMMAND'), 10, 'Heavy breastplate'])
		output = self.rpgJSON._runAction()
		self.assertTrue(output == {"error": {"message": _('ERROR_TAKE_QUANTITY_TOO_HIGH'), "code": 1}})

	def test_with_quantity_text(self):
		self.rpgText.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', [_('TAKE_COMMAND'), 2, 'Heavy breastplate'])
		output = self.rpgText._runAction()
		self.assertTrue(output == _('TAKE_CONFIRMATION_%(quantity)s_%(name)s') % {'quantity': 2, 'name': 'Heavy breastplate'})

	def test_with_quantity_json(self):
		self.rpgJSON.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', [_('TAKE_COMMAND'), 2, 'Heavy breastplate'])
		output = self.rpgJSON._runAction()
		self.assertTrue(output == {"name": "Heavy breastplate", "quantity": 2})

	def test_implied_quantity_text(self):
		self.rpgText.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', [_('TAKE_COMMAND'), 'Heavy breastplate'])
		output = self.rpgText._runAction()
		self.assertTrue(output == _('TAKE_CONFIRMATION_%(quantity)s_%(name)s') % {'quantity': 1, 'name': 'Heavy breastplate'})

	def test_implied_quantity_json(self):
		self.rpgJSON.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', [_('TAKE_COMMAND'), 'Heavy breastplate'])
		output = self.rpgJSON._runAction()
		self.assertTrue(output == {"name": "Heavy breastplate", "quantity": 1})

unittest.main()