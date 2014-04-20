# -*- coding: utf-8 -*-
import unittest
import sys
import os
sys.path.append(os.path.realpath(__file__ + "/../../../"))

import tests.common
from core.localisation import _
import json


class openTests(tests.common.common):
	def test_no_container_given_text(self):
		self.rpgText.setAction([_('OPEN_COMMAND')])
		output = self.rpgText._runAction()
		self.assertTrue(output == _('ERROR_OPEN_NO_CONTAINER_PROVIDED'))

	def test_no_container_given_json(self):
		self.rpgJSON.setAction([_('OPEN_COMMAND')])
		output = self.rpgJSON._runAction()
		self.assertTrue(output == {"error": {"message": _('ERROR_OPEN_NO_CONTAINER_PROVIDED'), "code": 1}})

	def test_container_not_found_here_text(self):
		self.rpgText.setAction([_('OPEN_COMMAND'), 'box'])
		output = self.rpgText._runAction()
		self.assertTrue(output == _('ERROR_OPEN_CONTAINER_NOT_AVAILABLE'))

	def test_container_not_found_here_json(self):
		self.rpgJSON.setAction([_('OPEN_COMMAND'), 'box'])
		output = self.rpgJSON._runAction()
		self.assertTrue(output == {"error": {"message": _('ERROR_OPEN_CONTAINER_NOT_AVAILABLE'), "code": 1}})

	def test_unknown_container_type_text(self):
		self.rpgText.setAction([_('OPEN_COMMAND'), 'some-container'])
		output = self.rpgText._runAction()
		self.assertTrue(output == _('ERROR_UNKNOWN_ITEM_CONTAINER_TYPE_LABEL'))

	def test_unknown_container_type_json(self):
		self.rpgJSON.setAction([_('OPEN_COMMAND'), 'some-container'])
		output = self.rpgJSON._runAction()
		self.assertTrue(output == {"error": {"message": _('ERROR_UNKNOWN_ITEM_CONTAINER_TYPE_LABEL'), "code": 1}})

	def test_multiple_container_of_given_type_text(self):
		self.rpgText.setAction([_('OPEN_COMMAND'), 'wardrobe'])
		output = self.rpgText._runAction()
		self.assertTrue(output == _('ERROR_OPEN_MULTIPLE_CONTAINERS_AVAILABLE'))

	def test_multiple_container_of_given_type_json(self):
		self.rpgJSON.setAction([_('OPEN_COMMAND'), 'wardrobe'])
		output = self.rpgJSON._runAction()
		self.assertTrue(output == {"error": {"message": _('ERROR_OPEN_MULTIPLE_CONTAINERS_AVAILABLE'), "code": 1}})

	def test_single_container_of_given_type_text(self):
		self.rpgText.setAction([_('OPEN_COMMAND'), 'chest'])
		output = self.rpgText._runAction()
		expected = [
			_('ITEMS_IN_CONTAINER_%s') % 'chest',
			'  4 Heavy breastplate'
		]
		self.assertTrue(output == '\n'.join(expected))

	def test_single_container_of_given_type_json(self):
		self.rpgJSON.setAction([_('OPEN_COMMAND'), 'chest'])
		output = self.rpgJSON._runAction()
		self.assertTrue(output == {'items': [{'name': 'Heavy breastplate', 'quantity': 4}], 'container_type': 'chest'})

	def test_container_number_provided_text(self):
		self.rpgText.setAction([_('OPEN_COMMAND'), 'wardrobe', 0])
		output = self.rpgText._runAction()
		self.assertTrue(output == _('ERROR_OPEN_INVALID_INDEX'))

		self.rpgText.setAction([_('OPEN_COMMAND'), 'chest', 1])
		output = self.rpgText._runAction()
		expected = [
			_('ITEMS_IN_CONTAINER_%s') % 'chest',
			'  4 Heavy breastplate'
		]
		self.assertTrue(output == '\n'.join(expected))

		self.rpgText.setAction([_('OPEN_COMMAND'), 'chest', 2])
		output = self.rpgText._runAction()
		self.assertTrue(output == _('ERROR_OPEN_INVALID_INDEX'))

		self.rpgText.setAction([_('OPEN_COMMAND'), 'wardrobe', 1])
		output = self.rpgText._runAction()
		expected = [
			_('ITEMS_IN_CONTAINER_%s') % 'wardrobe',
			'  4 Heavy breastplate'
		]
		self.assertTrue(output == '\n'.join(expected))

		self.rpgText.setAction([_('OPEN_COMMAND'), 'wardrobe', 2])
		output = self.rpgText._runAction()
		expected = [
			_('ITEMS_IN_CONTAINER_%s') % 'wardrobe',
			'  4 Mist potion'
		]
		self.assertTrue(output == '\n'.join(expected))

	def test_container_number_provided_json(self):
		self.rpgJSON.setAction([_('OPEN_COMMAND'), 'wardrobe', 0])
		output = self.rpgJSON._runAction()
		self.assertTrue(output == {"error": {"message": _('ERROR_OPEN_INVALID_INDEX'), "code": 1}})

		self.rpgJSON.setAction([_('OPEN_COMMAND'), 'chest', 1])
		output = self.rpgJSON._runAction()
		self.assertTrue(output == {'items': [{'name': 'Heavy breastplate', 'quantity': 4}], 'container_type': 'chest'})

		self.rpgJSON.setAction([_('OPEN_COMMAND'), 'chest', 2])
		output = self.rpgJSON._runAction()
		self.assertTrue(output == {"error": {"message": _('ERROR_OPEN_INVALID_INDEX'), "code": 1}})

		self.rpgJSON.setAction([_('OPEN_COMMAND'), 'wardrobe', 1])
		output = self.rpgJSON._runAction()
		self.assertTrue(output == {'items': [{'name': 'Heavy breastplate', 'quantity': 4}], 'container_type': 'wardrobe'})

		self.rpgJSON.setAction([_('OPEN_COMMAND'), 'wardrobe', 2])
		output = self.rpgJSON._runAction()
		self.assertTrue(output == {'items': [{'name': 'Mist potion', 'quantity': 4}], 'container_type': 'wardrobe'})
