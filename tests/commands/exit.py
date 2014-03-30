# -*- coding: utf-8 -*-
import unittest
import sys
import os
sys.path.append(os.path.realpath(__file__ + "/../../../"))

import tests.common
from tests.output_capturer import capturer


class exitTests(tests.common.common):
	def test_no_place_given_text(self):
		with capturer() as output:
			self.rpgText.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', ['exit'])
			self.rpgText._runAction()
		self.assertTrue(output == ['I can\'t exit out of nothing'])

	def test_no_place_given_json(self):
		with capturer() as output:
			self.rpgJSON.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', ['exit'])
			self.rpgJSON._runAction()
		self.assertTrue(output == ['{"error": {"message": "I can\'t exit out of nothing", "code": 1}}'])

	def test_place_not_available_text(self):
		with capturer() as output:
			self.rpgText.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', ['exit', 'cave'])
			self.rpgText._runAction()
		self.assertTrue(output == ['There is no such place here'])

	def test_no_place_given_json(self):
		with capturer() as output:
			self.rpgJSON.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', ['exit', 'cave'])
			self.rpgJSON._runAction()
		self.assertTrue(output == ['{"error": {"message": "There is no such place here", "code": 1}}'])

	def test_wrong_place_text(self):
		with capturer() as output:
			self.rpgText.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', ['exit', 'dummyplace'])
			self.rpgText._runAction()
		self.assertTrue(output == ['Unknown place type'])

	def test_wrong_place_given_json(self):
		with capturer() as output:
			self.rpgJSON.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', ['exit', 'dummyplace'])
			self.rpgJSON._runAction()
		self.assertTrue(output == ['{"error": {"message": "Unknown place type", "code": 1}}'])

	def test_when_still_out_text(self):
		self.rpgText.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', ['exit', 'dungeon'])
		with capturer() as output:
			self.rpgText._runAction()
		self.assertTrue(output == ['There is no such place here'])

	def test_when_still_out_json(self):
		self.rpgJSON.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', ['exit', 'dungeon'])
		with capturer() as output:
			self.rpgJSON._runAction()
		self.assertTrue(output == ['{"error": {"message": "There is no such place here", "code": 1}}'])

	def test_text(self):
		self.rpgText.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', ['enter', 'dungeon'])
		with capturer() as output:
			self.rpgText._runAction()
		self.rpgText.setAction(['exit', 'dungeon'])
		with capturer() as output:
			self.rpgText._runAction()
		self.assertTrue(output == ['You are now outside'])

	def test_json(self):
		self.rpgJSON.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', ['enter', 'dungeon'])
		with capturer() as output:
			self.rpgJSON._runAction()
		self.rpgJSON.setAction(['exit', 'dungeon'])
		with capturer() as output:
			self.rpgJSON._runAction()
		self.assertTrue(output == ['["You are now outside"]'])

unittest.main()
