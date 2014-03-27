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
			rpg.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', ['enter'])
			rpg._runAction()
		self.assertTrue(output == ['I can\'t enter into nothing'])

	def test_no_place_given_json(self):
		with capturer() as output:
			rpg = Rpg.Rpg(renderMode=Rpg.RENDER_JSON)
			rpg.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', ['enter'])
			rpg._runAction()
		self.assertTrue(output == ['{"error": {"message": "I can\'t enter into nothing", "code": 1}}'])

	def test_place_not_available_text(self):
		with capturer() as output:
			rpg = Rpg.Rpg(renderMode=Rpg.RENDER_TEXT)
			rpg.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', ['enter', 'cave'])
			rpg._runAction()
		self.assertTrue(output == ['There is no such place here'])

	def test_no_place_given_json(self):
		with capturer() as output:
			rpg = Rpg.Rpg(renderMode=Rpg.RENDER_JSON)
			rpg.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', ['enter', 'cave'])
			rpg._runAction()
		self.assertTrue(output == ['{"error": {"message": "There is no such place here", "code": 1}}'])

	def test_wrong_place_text(self):
		with capturer() as output:
			rpg = Rpg.Rpg(renderMode=Rpg.RENDER_TEXT)
			rpg.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', ['enter', 'dummyplace'])
			rpg._runAction()
		self.assertTrue(output == ['Unknown place type'])

	def test_wrong_place_given_json(self):
		with capturer() as output:
			rpg = Rpg.Rpg(renderMode=Rpg.RENDER_JSON)
			rpg.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', ['enter', 'dummyplace'])
			rpg._runAction()
		self.assertTrue(output == ['{"error": {"message": "Unknown place type", "code": 1}}'])

	def test_text(self):
		with capturer() as output:
			rpg = Rpg.Rpg(renderMode=Rpg.RENDER_TEXT)
			rpg.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', ['enter', 'dungeon'])
			rpg._runAction()
		self.assertTrue(output == ['You enter.'])

	def test_json(self):
		with capturer() as output:
			rpg = Rpg.Rpg(renderMode=Rpg.RENDER_JSON)
			rpg.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', ['enter', 'dungeon'])
			rpg._runAction()
		self.assertTrue(output == ['["You enter."]'])

unittest.main()
