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
		self.rpgText.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', [_('LOOK_COMMAND')])
		output = self.rpgText._runAction()
		self.assertTrue(output ==
			_('CURRENT_REGION_%s') % 'The High lands\n' +\
			'\n' +\
			_('PRESENT_CHARACTERS') +'\n'+\
			'    Tom\n' +\
			'\n' +\
			_('AVAILABLE_DIRECTIONS') +'\n'+\
			'    ' + _('DIRECTION_KEY_NORTH') +'\n'+\
			'\n' +\
			_('AVAILABLE_PLACES') +'\n'+\
			'    first dungeon\n' +\
			'\n' +\
			_('AVAILABLE_ITEMS') +'\n'+\
			'  6 Heavy breastplate'
		)

	def test_json(self):
		self.rpgJSON.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', [_('LOOK_COMMAND')])
		output = self.rpgJSON._runAction()
		self.assertTrue(output == {
			"directions": [_('DIRECTION_KEY_NORTH')],
			"items": [{"name": "Heavy breastplate", "quantity": 6}],
			"region": "The High lands",
			"places": ["first dungeon"],
			"characters": ["Tom"]
		})

unittest.main()
