# -*- coding: utf-8 -*-
import unittest

import tests.common
from core.localisation import _
import json


class lookTests(tests.common.common):
	def test_text(self):
		self.rpgText.setAction([_('LOOK_COMMAND')])
		output = self.rpgText._runAction()
		self.assertEquals(output,
			_('CURRENT_REGION_%s') % 'The High lands\n' +\
			_('AREA_HAS_SAVE_POINT') +\
			'\n\n' +\
			_('PRESENT_CHARACTERS') +'\n'+\
			'    Tom\n' +\
			'\n' +\
			_('AVAILABLE_DIRECTIONS') +'\n'+\
			'    ' + _('DIRECTION_KEY_SOUTH') +'\n'+\
			'\n' +\
			_('AVAILABLE_PLACES') +'\n'+\
			'    first cave\n' +\
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
		self.assertEquals(output, {
			"directions": [_('DIRECTION_KEY_SOUTH')],
			"items": [{"name": "Heavy breastplate", "quantity": 6}],
			"region": {
				"has_save_point": True,
				"name": "The High lands",
				"x": 0,
				"y": 1
			},
			"places": ["first cave", "first dungeon"],
			"characters": ["Tom"],
			"item_containers": {'chest': 1, 'wardrobe': 2}
		})

	def test_unknown_section_text(self):
		self.rpgText.setAction([_('LOOK_COMMAND'), 'foo'])
		output = self.rpgText._runAction()
		self.assertEquals(output, _('ERROR_LOOK_UNKNOWN_SECTION'))

	def test_unknown_section_json(self):
		self.rpgJSON.setAction([_('LOOK_COMMAND'), 'foo'])
		output = self.rpgJSON._runAction()
		self.assertEquals(output, {"error": {"message": _('ERROR_LOOK_UNKNOWN_SECTION'), "code": 1}})

	def test_region_text(self):
		self.rpgText.setAction([_('LOOK_COMMAND'), _('LOOK_REGION_PARAM')])
		output = self.rpgText._runAction()
		expected = [
			_('CURRENT_REGION_%s') % 'The High lands',
			_('AREA_HAS_SAVE_POINT')
		]
		self.assertEquals(output, '\n'.join(expected))

	def test_region_json(self):
		self.rpgJSON.setAction([_('LOOK_COMMAND'), _('LOOK_REGION_PARAM')])
		output = self.rpgJSON._runAction()
		self.assertEquals(output, {"region": {"has_save_point": True, "name": "The High lands", "x": 0, "y": 1}})

	def test_characters_text(self):
		self.rpgText.setAction([_('LOOK_COMMAND'), _('LOOK_CHARACTERS_PARAM')])
		output = self.rpgText._runAction()
		self.assertEquals(output, _('PRESENT_CHARACTERS') + '\n    Tom')

	def test_characters_json(self):
		self.rpgJSON.setAction([_('LOOK_COMMAND'), _('LOOK_CHARACTERS_PARAM')])
		output = self.rpgJSON._runAction()
		self.assertEquals(output, {"characters": ["Tom"]})

	def test_directions_text(self):
		self.rpgText.setAction([_('LOOK_COMMAND'), _('LOOK_DIRECTIONS_PARAM')])
		output = self.rpgText._runAction()
		self.assertEquals(
			output, _('AVAILABLE_DIRECTIONS') + '\n    ' +\
				_('DIRECTION_KEY_SOUTH')
		)

	def test_directions_json(self):
		self.rpgJSON.setAction([_('LOOK_COMMAND'), _('LOOK_DIRECTIONS_PARAM')])
		output = self.rpgJSON._runAction()
		self.assertEquals(output, {"directions": [_('DIRECTION_KEY_SOUTH')]})

	def test_places_text(self):
		self.rpgText.setAction([_('LOOK_COMMAND'), _('LOOK_PLACES_PARAM')])
		output = self.rpgText._runAction()
		self.assertEquals(output, _('AVAILABLE_PLACES') +'\n    first cave' +'\n    first dungeon')

	def test_places_json(self):
		self.rpgJSON.setAction([_('LOOK_COMMAND'), _('LOOK_PLACES_PARAM')])
		output = self.rpgJSON._runAction()
		self.assertEquals(output, {"places": ["first cave", "first dungeon"]})

	def test_objects_text(self):
		self.rpgText.setAction([_('LOOK_COMMAND'), _('LOOK_OBJECTS_PARAM')])
		output = self.rpgText._runAction()
		self.assertEquals(output, _('AVAILABLE_ITEMS') +'\n'+\
			'  6 Heavy breastplate')

	def test_objects_json(self):
		self.rpgJSON.setAction([_('LOOK_COMMAND'), _('LOOK_OBJECTS_PARAM')])
		output = self.rpgJSON._runAction()
		self.assertEquals(output, {"items": [{"name": "Heavy breastplate", "quantity": 6}]})

	def test_containers_text(self):
		self.rpgText.setAction([_('LOOK_COMMAND'), _('LOOK_CONTAINERS_PARAM')])
		output = self.rpgText._runAction()
		self.assertEquals(output, _('AVAILABLE_ITEMS_CONTAINERS') +'\n'+\
			'    chest #1\n' +\
			'    wardrobe #1\n' +\
			'    wardrobe #2')

	def test_containers_json(self):
		self.rpgJSON.setAction([_('LOOK_COMMAND'), _('LOOK_CONTAINERS_PARAM')])
		output = self.rpgJSON._runAction()
		self.assertEquals(output, {"item_containers": {'chest': 1, 'wardrobe': 2}})

	def test_no_enemy_text(self):
		self.rpgText.setAction([_('LOOK_COMMAND'), _('LOOK_FIGHT_PARAM')])
		output = self.rpgText._runAction()
		self.assertEquals(output, '')

	def test_no_enemy_json(self):
		self.rpgJSON.setAction([_('LOOK_COMMAND'), _('LOOK_FIGHT_PARAM')])
		output = self.rpgJSON._runAction()
		self.assertEquals(output, {'fight': None})

	def test_enemies_text(self):
		self.rpgText.setAction([_('MOVE_COMMAND'), _('DIRECTION_KEY_SOUTH')])
		self.rpgText._runAction()
		self.rpgText.setAction([_('MOVE_COMMAND'), _('DIRECTION_KEY_EAST')])
		self.rpgText._runAction()
		self.rpgText.setAction([_('LOOK_COMMAND'), _('LOOK_FIGHT_PARAM')])
		output = self.rpgText._runAction()
		self.assertEquals(output, _('CURRENTLY_FIGHTING_%s') % 'rat')

	def test_enemies_json(self):
		self.rpgJSON.setAction([_('MOVE_COMMAND'), _('DIRECTION_KEY_SOUTH')])
		self.rpgJSON._runAction()
		self.rpgJSON.setAction([_('MOVE_COMMAND'), _('DIRECTION_KEY_EAST')])
		self.rpgJSON._runAction()
		self.rpgJSON.setAction([_('LOOK_COMMAND'), _('LOOK_FIGHT_PARAM')])
		output = self.rpgJSON._runAction()
		self.assertEquals(output, {'fight': {'name': 'rat', 'stat_defence': 2, 'stat_attack': 2, 'stat_max_hp': 15, 'stat_current_hp': 15, 'stat_speed': 1, 'stat_luck': 25}})

	def test_no_save_point_json(self):
		self.rpgJSON.setAction([_('MOVE_COMMAND'), _('DIRECTION_KEY_SOUTH')])
		self.rpgJSON._runAction()
		self.rpgJSON.setAction([_('MOVE_COMMAND'), _('DIRECTION_KEY_SOUTH')])
		self.rpgJSON._runAction()
		self.rpgJSON.setAction([_('LOOK_COMMAND'), _('LOOK_REGION_PARAM')])
		output = self.rpgJSON._runAction()
		self.assertEquals(output['region']['has_save_point'], False)
