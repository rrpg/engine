# -*- coding: utf-8 -*-
import unittest
import sys
import os
sys.path.append(os.path.realpath(__file__ + "/../../../"))

import tests.common
from tests.output_capturer import capturer


class dropTests(tests.common.common):
	def test_no_item_given_text(self):
		with capturer() as output:
			self.rpgText.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', ['drop'])
			self.rpgText._runAction()
		self.assertTrue(output == ['What shall I drop?'])

	def test_no_item_given_json(self):
		with capturer() as output:
			self.rpgJSON.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', ['drop'])
			self.rpgJSON._runAction()
		self.assertTrue(output == ['{"error": {"message": "What shall I drop?", "code": 1}}'])

	def test_unknown_item_text(self):
		with capturer() as output:
			self.rpgText.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', ['drop', 'some dummy item'])
			self.rpgText._runAction()
		self.assertTrue(output == ['I have none of those'])

	def test_unknown_item_json(self):
		with capturer() as output:
			self.rpgJSON.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', ['drop', 'some dummy item'])
			self.rpgJSON._runAction()
		self.assertTrue(output == ['{"error": {"message": "I have none of those", "code": 1}}'])

	def test_item_not_here_text(self):
		with capturer() as output:
			self.rpgText.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', ['drop', 'Mist potion'])
			self.rpgText._runAction()
		self.assertTrue(output == ['I have none of those'])

	def test_item_not_here_json(self):
		with capturer() as output:
			self.rpgJSON.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', ['drop', 'Mist potion'])
			self.rpgJSON._runAction()
		self.assertTrue(output == ['{"error": {"message": "I have none of those", "code": 1}}'])

	def test_quantity_too_high_text(self):
		self.rpgText.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER')
		self.rpgText.setAction(['take', 2, 'Heavy breastplate'])
		with capturer() as output:
			self.rpgText._runAction()
		with capturer() as output:
			self.rpgText.setAction(['drop', 10, 'Heavy breastplate'])
			self.rpgText._runAction()
		self.assertTrue(output == ['I don\'t have enough Heavy breastplate to drop'])

	def test_quantity_too_high_json(self):
		self.rpgJSON.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER')
		self.rpgJSON.setAction(['take', 2, 'Heavy breastplate'])
		with capturer() as output:
			self.rpgJSON._runAction()
		with capturer() as output:
			self.rpgJSON.setAction(['drop', 10, 'Heavy breastplate'])
			self.rpgJSON._runAction()
		self.assertTrue(output == ['{"error": {"message": "I don\'t have enough Heavy breastplate to drop", "code": 1}}'])

	def test_with_quantity_text(self):
		self.rpgText.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER')
		self.rpgText.setAction(['take', 2, 'Heavy breastplate'])
		with capturer() as output:
			self.rpgText._runAction()
		with capturer() as output:
			self.rpgText.setAction(['drop', 2, 'Heavy breastplate'])
			self.rpgText._runAction()
		self.assertTrue(output == ['You drop 2 Heavy breastplate'])

	def test_with_quantity_json(self):
		self.rpgJSON.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER')
		self.rpgJSON.setAction(['take', 2, 'Heavy breastplate'])
		with capturer() as output:
			self.rpgJSON._runAction()
		with capturer() as output:
			self.rpgJSON.setAction(['drop', 2, 'Heavy breastplate'])
			self.rpgJSON._runAction()
		self.assertTrue(output == ['{"name": "Heavy breastplate", "quantity": 2}'])

	def test_implied_quantity_text(self):
		self.rpgText.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER')
		self.rpgText.setAction(['take', 'Heavy breastplate'])
		with capturer() as output:
			self.rpgText._runAction()
		with capturer() as output:
			self.rpgText.setAction(['drop', 'Heavy breastplate'])
			self.rpgText._runAction()
		self.assertTrue(output == ['You drop 1 Heavy breastplate'])

	def test_implied_quantity_json(self):
		self.rpgJSON.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER')
		self.rpgJSON.setAction(['take', 'Heavy breastplate'])
		with capturer() as output:
			self.rpgJSON._runAction()
		with capturer() as output:
			self.rpgJSON.setAction(['drop', 'Heavy breastplate'])
			self.rpgJSON._runAction()
		self.assertTrue(output == ['{"name": "Heavy breastplate", "quantity": 1}'])

unittest.main()
