# -*- coding: utf-8 -*-
import unittest
import sys
import os
sys.path.append(os.path.realpath(__file__ + "/../../../"))

import tests.common
from tests.output_capturer import capturer


class enterTests(tests.common.common):
	def test_empty_text(self):
		with capturer() as output:
			self.rpgText.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', ['inventory'])
			self.rpgText._runAction()
		self.assertTrue(output == [])

	def test_empty_json(self):
		with capturer() as output:
			self.rpgJSON.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', ['inventory'])
			self.rpgJSON._runAction()
		self.assertTrue(output == ['[]'])

	def test_not_empty_text(self):
		self.rpgText.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER')
		with capturer() as output:
			self.rpgText.setAction(['take', 2, 'Heavy breastplate'])
			self.rpgText._runAction()
		with capturer() as output:
			self.rpgText.setAction(['inventory'])
			self.rpgText._runAction()
		self.assertTrue(output == ['  2 Heavy breastplate'])

	def test_not_empty_json(self):
		self.rpgJSON.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER')
		with capturer() as output:
			self.rpgJSON.setAction(['take', 2, 'Heavy breastplate'])
			self.rpgJSON._runAction()
		with capturer() as output:
			self.rpgJSON.setAction(['inventory'])
			self.rpgJSON._runAction()
		self.assertTrue(output == ['[{"name": "Heavy breastplate", "quantity": 2}]'])

unittest.main()
