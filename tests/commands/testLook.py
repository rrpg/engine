# -*- coding: utf-8 -*-
import unittest
import sys
import os

sys.path.append(os.path.realpath(os.path.dirname(__file__) + "/../../"))

import tests.common
from core.localisation import _
import json


class lookTests(tests.common.common):
	def test_text(self):
		self.rpgText.setAction([_('LOOK_COMMAND')])
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
			'  6 Heavy breastplate\n' +\
			'\n' +\
			_('AVAILABLE_ITEMS_CONTAINERS') +'\n'+\
			'    chest #0\n' +\
			'    wardrobe #1\n' +\
			'    wardrobe #2'
		)

	def test_json(self):
		self.rpgJSON.setAction([_('LOOK_COMMAND')])
		output = self.rpgJSON._runAction()
		self.assertTrue(output == {
			"directions": [_('DIRECTION_KEY_NORTH')],
			"items": [{"name": "Heavy breastplate", "quantity": 6}],
			"region": "The High lands",
			"places": ["first dungeon"],
			"characters": ["Tom"],
			"item_containers": [[0, 'chest'], [1, 'wardrobe'], [2, 'wardrobe']]
		})

