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
			'    chest #1\n' +\
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
			"item_containers": {'chest': 1, 'wardrobe': 2}
		})

	def test_unknown_section_text(self):
		self.rpgText.setAction([_('LOOK_COMMAND'), 'foo'])
		output = self.rpgText._runAction()
		self.assertTrue(output == _('ERROR_LOOK_UNKNOWN_SECTION'))

	def test_unknown_section_json(self):
		self.rpgJSON.setAction([_('LOOK_COMMAND'), 'foo'])
		output = self.rpgJSON._runAction()
		self.assertTrue(output == {"error": {"message": _('ERROR_LOOK_UNKNOWN_SECTION'), "code": 1}})


	def test_region_text(self):
		self.rpgText.setAction([_('LOOK_COMMAND'), _('LOOK_REGION_PARAM')])
		output = self.rpgText._runAction()
		self.assertTrue(output == _('CURRENT_REGION_%s') % 'The High lands')

	def test_region_json(self):
		self.rpgJSON.setAction([_('LOOK_COMMAND'), _('LOOK_REGION_PARAM')])
		output = self.rpgJSON._runAction()
		self.assertTrue(output == {"region": "The High lands"})

	def test_characters_text(self):
		self.rpgText.setAction([_('LOOK_COMMAND'), _('LOOK_CHARACTERS_PARAM')])
		output = self.rpgText._runAction()
		self.assertTrue(output == _('PRESENT_CHARACTERS') + '\n    Tom')

	def test_characters_json(self):
		self.rpgJSON.setAction([_('LOOK_COMMAND'), _('LOOK_CHARACTERS_PARAM')])
		output = self.rpgJSON._runAction()
		self.assertTrue(output == {"characters": ["Tom"]})

	def test_directions_text(self):
		self.rpgText.setAction([_('LOOK_COMMAND'), _('LOOK_DIRECTIONS_PARAM')])
		output = self.rpgText._runAction()
		self.assertTrue(
			output == _('AVAILABLE_DIRECTIONS') + '\n    ' +\
				_('DIRECTION_KEY_NORTH')
		)

	def test_directions_json(self):
		self.rpgJSON.setAction([_('LOOK_COMMAND'), _('LOOK_DIRECTIONS_PARAM')])
		output = self.rpgJSON._runAction()
		self.assertTrue(output == {"directions": [_('DIRECTION_KEY_NORTH')]})

	def test_places_text(self):
		self.rpgText.setAction([_('LOOK_COMMAND'), _('LOOK_PLACES_PARAM')])
		output = self.rpgText._runAction()
		self.assertTrue(output == _('AVAILABLE_PLACES') +'\n    first dungeon')

	def test_places_json(self):
		self.rpgJSON.setAction([_('LOOK_COMMAND'), _('LOOK_PLACES_PARAM')])
		output = self.rpgJSON._runAction()
		self.assertTrue(output == {"places": ["first dungeon"]})

	def test_objects_text(self):
		self.rpgText.setAction([_('LOOK_COMMAND'), _('LOOK_OBJECTS_PARAM')])
		output = self.rpgText._runAction()
		self.assertTrue(output == _('AVAILABLE_ITEMS') +'\n'+\
			'  6 Heavy breastplate')

	def test_objects_json(self):
		self.rpgJSON.setAction([_('LOOK_COMMAND'), _('LOOK_OBJECTS_PARAM')])
		output = self.rpgJSON._runAction()
		self.assertTrue(output == {"items": [{"name": "Heavy breastplate", "quantity": 6}]})

	def test_containers_text(self):
		self.rpgText.setAction([_('LOOK_COMMAND'), _('LOOK_CONTAINERS_PARAM')])
		output = self.rpgText._runAction()
		self.assertTrue(output == _('AVAILABLE_ITEMS_CONTAINERS') +'\n'+\
			'    chest #1\n' +\
			'    wardrobe #1\n' +\
			'    wardrobe #2')

	def test_containers_json(self):
		self.rpgJSON.setAction([_('LOOK_COMMAND'), _('LOOK_CONTAINERS_PARAM')])
		output = self.rpgJSON._runAction()
		self.assertTrue(output == {"item_containers": {'chest': 1, 'wardrobe': 2}})
