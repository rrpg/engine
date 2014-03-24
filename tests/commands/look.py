import unittest
import sys
import os
sys.path.append(os.path.realpath(__file__ + "/../../../"))

from tests.output_capturer import capturer

from models import player
from core import Rpg
from core.commands import look

class lookTests(unittest.TestCase):
	def setUp(self):
		pass

	def test_normal(self):
		with capturer() as output:
			rpg = Rpg.Rpg(False, Rpg.RENDER_TEXT)
			rpg.init(os.path.realpath(__file__ + "/../../../database/rpg.db"), 'TEST_PLAYER', 'TEST_PLAYER', ['look'])
			rpg._runAction()
		self.assertTrue(output == ['You are in The High lands', '', 'You see these characters arround:', '    Tom', '', 'You can go in the following directions:', '    north', '', 'You see the following items', '  2 Heavy breastplate'])

	def test_json(self):
		with capturer() as output:
			rpg = Rpg.Rpg(False, Rpg.RENDER_JSON)
			rpg.init(os.path.realpath(__file__ + "/../../../database/rpg.db"), 'TEST_PLAYER', 'TEST_PLAYER', ['look'])
			rpg._runAction()
		self.assertTrue(output == ['{"directions": ["north"], "items": [{"name": "Heavy breastplate", "quantity": 2}], "region": "The High lands", "places": [], "characters": ["Tom"]}'])

unittest.main()
