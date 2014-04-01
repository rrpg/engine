# -*- coding: utf-8 -*-
import unittest
import sys
import os
sys.path.append(os.path.realpath(__file__ + "/../../../"))

import tests.common
from tests.output_capturer import capturer
from core.localisation import _
import json


class enterTests(tests.common.common):
	def test_empty_text(self):
		with capturer() as output:
			self.rpgText.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', [_('INVENTORY_COMMAND')])
			self.rpgText._runAction()
		self.assertTrue(output == [])

	def test_empty_json(self):
		with capturer() as output:
			self.rpgJSON.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', [_('INVENTORY_COMMAND')])
			self.rpgJSON._runAction()
		self.assertTrue(output == ['[]'])

	def test_not_empty_text(self):
		self.rpgText.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER')
		with capturer() as output:
			self.rpgText.setAction([_('TAKE_COMMAND'), 2, 'Heavy breastplate'])
			self.rpgText._runAction()
		with capturer() as output:
			self.rpgText.setAction([_('INVENTORY_COMMAND')])
			self.rpgText._runAction()
		self.assertTrue(output == ['  2 Heavy breastplate'])

	def test_not_empty_json(self):
		self.rpgJSON.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER')
		with capturer() as output:
			self.rpgJSON.setAction([_('TAKE_COMMAND'), 2, 'Heavy breastplate'])
			self.rpgJSON._runAction()
		with capturer() as output:
			self.rpgJSON.setAction([_('INVENTORY_COMMAND')])
			self.rpgJSON._runAction()
		self.assertTrue(json.loads(output[0]) == [{"name": "Heavy breastplate", "quantity": 2}])

unittest.main()
