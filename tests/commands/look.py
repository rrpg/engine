# -*- coding: utf-8 -*-
import unittest
import sys
import os

sys.path.append(os.path.realpath(os.path.dirname(__file__) + "/../../"))

import tests.common
from tests.output_capturer import capturer
from core.localisation import _
import json


class lookTests(tests.common.common):
	def test_text(self):
		with capturer() as output:
			self.rpgText.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', [_('LOOK_COMMAND')])
			self.rpgText._runAction()
		self.assertTrue(output == [
			_('CURRENT_REGION_%s') % 'The High lands',
			'',
			_('PRESENT_CHARACTERS'),
			'    Tom',
			'',
			_('AVAILABLE_DIRECTIONS'),
			'    ' + _('DIRECTION_KEY_NORTH'),
			'',
			_('AVAILABLE_PLACES'),
			'    first dungeon',
			'',
			_('AVAILABLE_ITEMS'),
			'  6 Heavy breastplate'
		])

	def test_json(self):
		with capturer() as output:
			self.rpgJSON.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', [_('LOOK_COMMAND')])
			self.rpgJSON._runAction()
		self.assertTrue(json.loads(output[0]) == {
			"directions": [_('DIRECTION_KEY_NORTH')],
			"items": [{"name": "Heavy breastplate", "quantity": 6}],
			"region": "The High lands",
			"places": ["first dungeon"],
			"characters": ["Tom"]
		})

unittest.main()
