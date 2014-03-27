import unittest
import sys
import os

sys.path.append(os.path.realpath(os.path.dirname(__file__) + "/../../"))

import tests.common
from tests.output_capturer import capturer

from core import Rpg

class lookTests(tests.common.common):
	def test_text(self):
		with capturer() as output:
			rpg = Rpg.Rpg(renderMode=Rpg.RENDER_TEXT)
			rpg.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', ['look'])
			rpg._runAction()
		self.assertTrue(output == [
			'You are in The High lands',
			'',
			'You see these characters arround:',
			'    Tom',
			'',
			'You can go in the following directions:',
			'    north',
			'',
			'You see the following places:',
			'    first dungeon',
			'',
			'You see the following items',
			'  6 Heavy breastplate'
		])

	def test_json(self):
		with capturer() as output:
			rpg = Rpg.Rpg(renderMode=Rpg.RENDER_JSON)
			rpg.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', ['look'])
			rpg._runAction()
		self.assertTrue(output == ['{"directions": ["north"], "items": [{"name": "Heavy breastplate", "quantity": 6}], "region": "The High lands", "places": ["first dungeon"], "characters": ["Tom"]}'])

unittest.main()
