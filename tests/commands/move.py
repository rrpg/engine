# -*- coding: utf-8 -*-
import unittest
import sys
import os
sys.path.append(os.path.realpath(__file__ + "/../../../"))

import tests.common
from tests.output_capturer import capturer


class moveTests(tests.common.common):
	def test_no_direction_given_text(self):
		with capturer() as output:
			self.rpgText.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', ['move'])
			self.rpgText._runAction()
		self.assertTrue(output == ['Where shall I go?'])

	def test_no_direction_given_json(self):
		with capturer() as output:
			self.rpgJSON.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', ['move'])
			self.rpgJSON._runAction()
		self.assertTrue(output == ['{"error": {"message": "Where shall I go?", "code": 1}}'])

	def test_invalid_direction_text(self):
		with capturer() as output:
			self.rpgText.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', ['move', 'bad-direction'])
			self.rpgText._runAction()
		self.assertTrue(output == ['bad-direction is not a valid direction'])

	def test_invalid_direction_json(self):
		with capturer() as output:
			self.rpgJSON.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', ['move', 'bad-direction'])
			self.rpgJSON._runAction()
		self.assertTrue(output == ['{"error": {"message": "bad-direction is not a valid direction", "code": 1}}'])

	def test_not_available_direction_text(self):
		with capturer() as output:
			self.rpgText.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', ['move', 'east'])
			self.rpgText._runAction()
		self.assertTrue(output == ['I can\'t go there'])

	def test_not_available_direction_json(self):
		with capturer() as output:
			self.rpgJSON.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', ['move', 'east'])
			self.rpgJSON._runAction()
		self.assertTrue(output == ['{"error": {"message": "I can\'t go there", "code": 1}}'])

	def test_text(self):
		with capturer() as output:
			self.rpgText.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', ['move', 'north'])
			self.rpgText._runAction()
		self.assertTrue(output == ['lets go north'])

	def test_json(self):
		with capturer() as output:
			self.rpgJSON.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', ['move', 'north'])
			self.rpgJSON._runAction()
		self.assertTrue(output == ['{"direction": "north"}'])

unittest.main()
