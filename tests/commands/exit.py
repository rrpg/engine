import unittest
import sys
import os
sys.path.append(os.path.realpath(__file__ + "/../../../"))

import tests.common
from tests.output_capturer import capturer

from core import Rpg

class enterTests(tests.common.common):
	def test_no_place_given_text(self):
		with capturer() as output:
			rpg = Rpg.Rpg(renderMode=Rpg.RENDER_TEXT)
			rpg.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', ['exit'])
			rpg._runAction()
		self.assertTrue(output == ['I can\'t exit out of nothing'])

	def test_no_place_given_json(self):
		with capturer() as output:
			rpg = Rpg.Rpg(renderMode=Rpg.RENDER_JSON)
			rpg.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', ['exit'])
			rpg._runAction()
		self.assertTrue(output == ['{"error": {"message": "I can\'t exit out of nothing", "code": 1}}'])

	def test_place_not_available_text(self):
		with capturer() as output:
			rpg = Rpg.Rpg(renderMode=Rpg.RENDER_TEXT)
			rpg.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', ['exit', 'cave'])
			rpg._runAction()
		self.assertTrue(output == ['There is no such place here'])

	def test_no_place_given_json(self):
		with capturer() as output:
			rpg = Rpg.Rpg(renderMode=Rpg.RENDER_JSON)
			rpg.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', ['exit', 'cave'])
			rpg._runAction()
		self.assertTrue(output == ['{"error": {"message": "There is no such place here", "code": 1}}'])

	def test_wrong_place_text(self):
		with capturer() as output:
			rpg = Rpg.Rpg(renderMode=Rpg.RENDER_TEXT)
			rpg.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', ['exit', 'dummyplace'])
			rpg._runAction()
		self.assertTrue(output == ['Unknown place type'])

	def test_wrong_place_given_json(self):
		with capturer() as output:
			rpg = Rpg.Rpg(renderMode=Rpg.RENDER_JSON)
			rpg.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', ['exit', 'dummyplace'])
			rpg._runAction()
		self.assertTrue(output == ['{"error": {"message": "Unknown place type", "code": 1}}'])

	def test_when_still_out_text(self):
		rpg = Rpg.Rpg(renderMode=Rpg.RENDER_TEXT)
		rpg.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', ['exit', 'dungeon'])
		with capturer() as output:
			rpg._runAction()
		self.assertTrue(output == ['There is no such place here'])

	def test_when_still_out_json(self):
		rpg = Rpg.Rpg(renderMode=Rpg.RENDER_JSON)
		rpg.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', ['exit', 'dungeon'])
		with capturer() as output:
			rpg._runAction()
		self.assertTrue(output == ['{"error": {"message": "There is no such place here", "code": 1}}'])

	def test_text(self):
		rpg = Rpg.Rpg(renderMode=Rpg.RENDER_TEXT)
		rpg.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', ['enter', 'dungeon'])
		with capturer() as output:
			rpg._runAction()
		rpg.setAction(['exit', 'dungeon'])
		with capturer() as output:
			rpg._runAction()
		self.assertTrue(output == ['You are now outside'])

	def test_json(self):
		rpg = Rpg.Rpg(renderMode=Rpg.RENDER_JSON)
		rpg.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', ['enter', 'dungeon'])
		with capturer() as output:
			rpg._runAction()
		rpg.setAction(['exit', 'dungeon'])
		with capturer() as output:
			rpg._runAction()
		self.assertTrue(output == ['["You are now outside"]'])

unittest.main()
