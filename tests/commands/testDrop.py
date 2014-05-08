# -*- coding: utf-8 -*-
import unittest
import sys
import os
sys.path.append(os.path.realpath(__file__ + "/../../../"))

import tests.common
from core.localisation import _
import json


class dropTests(tests.common.common):
	# Quantity tests
	def test_invalid_quantity_text(self):
		self.rpgText.setAction([_('DROP_COMMAND'), 'ten', 'Heavy breastplate', 'chest', 1])
		output = self.rpgText._runAction()
		self.assertTrue(output == _('ERROR_DROP_INVALID_FORMAT_QUANTITY'))

	def test_invalid_quantity_json(self):
		self.rpgJSON.setAction([_('DROP_COMMAND'), 'ten', 'Heavy breastplate', 'chest', 1])
		output = self.rpgJSON._runAction()
		self.assertTrue(output == {"error": {"message": _('ERROR_DROP_INVALID_FORMAT_QUANTITY'), "code": 1}})

	def test_quantity_too_low_text(self):
		self.rpgText.setAction([_('DROP_COMMAND'), 0, 'Heavy breastplate'])
		output = self.rpgText._runAction()
		self.assertTrue(output == _('ERROR_DROP_TOO_LOW_QUANTITY'))

	def test_quantity_too_low_json(self):
		self.rpgJSON.setAction([_('DROP_COMMAND'), 0, 'Heavy breastplate'])
		output = self.rpgJSON._runAction()
		self.assertTrue(output == {"error": {"message": _('ERROR_DROP_TOO_LOW_QUANTITY'), "code": 1}})

	def test_quantity_too_high_text(self):
		self.rpgText.setAction([_('TAKE_COMMAND'), 2, 'Heavy breastplate'])
		self.rpgText._runAction()
		self.rpgText.setAction([_('DROP_COMMAND'), 10, 'Heavy breastplate'])
		output = self.rpgText._runAction()
		self.assertTrue(output == _('ERROR_DROP_QUANTITY_TOO_HIGH_%s') % 'Heavy breastplate')

	def test_quantity_too_high_json(self):
		self.rpgJSON.setAction([_('TAKE_COMMAND'), 2, 'Heavy breastplate'])
		self.rpgJSON._runAction()
		self.rpgJSON.setAction([_('DROP_COMMAND'), 10, 'Heavy breastplate'])
		output = self.rpgJSON._runAction()
		self.assertTrue(output == {"error": {"message": _('ERROR_DROP_QUANTITY_TOO_HIGH_%s') % 'Heavy breastplate', "code": 1}})

	# Items tests
	def test_item_missing_text(self):
		self.rpgText.setAction([_('DROP_COMMAND')])
		output = self.rpgText._runAction()
		self.assertTrue(output == _('ERROR_DROP_NO_ITEM_GIVEN'))

	def test_item_missing_json(self):
		self.rpgJSON.setAction([_('DROP_COMMAND')])
		output = self.rpgJSON._runAction()
		self.assertTrue(output == {"error": {"message": _('ERROR_DROP_NO_ITEM_GIVEN'), "code": 1}})

	def test_item_missing_with_quantity_text(self):
		self.rpgText.setAction([_('DROP_COMMAND'), 1])
		output = self.rpgText._runAction()
		self.assertTrue(output == _('ERROR_DROP_NO_ITEM_GIVEN'))

	def test_item_missing_with_quantity_json(self):
		self.rpgJSON.setAction([_('DROP_COMMAND'), 1])
		output = self.rpgJSON._runAction()
		self.assertTrue(output == {"error": {"message": _('ERROR_DROP_NO_ITEM_GIVEN'), "code": 1}})

	def test_unknown_item_text(self):
		self.rpgText.setAction([_('DROP_COMMAND'), 'some dummy item'])
		output = self.rpgText._runAction()
		self.assertTrue(output == _('ERROR_DROP_UNKNOWN_ITEM'))

	def test_unknown_item_json(self):
		self.rpgJSON.setAction([_('DROP_COMMAND'), 'some dummy item'])
		output = self.rpgJSON._runAction()
		self.assertTrue(output == {"error": {"message": _('ERROR_DROP_UNKNOWN_ITEM'), "code": 1}})

	def test_not_available_item_text(self):
		self.rpgText.setAction([_('DROP_COMMAND'), 'Mist potion'])
		output = self.rpgText._runAction()
		self.assertTrue(output == _('ERROR_DROP_ITEM_NOT_AVAILABLE'))

	def test_not_available_item_json(self):
		self.rpgJSON.setAction([_('DROP_COMMAND'), 'Mist potion'])
		output = self.rpgJSON._runAction()
		self.assertTrue(output == {"error": {"message": _('ERROR_DROP_ITEM_NOT_AVAILABLE'), "code": 1}})

	# Container tests
	def test_unknown_container_type_text(self):
		self.rpgText.setAction([_('TAKE_COMMAND'), 'Heavy breastplate'])
		self.rpgText._runAction()
		self.rpgText.setAction([_('DROP_COMMAND'), 'Heavy breastplate', 'some container'])
		output = self.rpgText._runAction()
		self.assertTrue(output == _('ERROR_UNKNOWN_ITEM_CONTAINER_TYPE_LABEL'))

	def test_unknown_container_type_json(self):
		self.rpgJSON.setAction([_('TAKE_COMMAND'), 'Heavy breastplate'])
		self.rpgJSON._runAction()
		self.rpgJSON.setAction([_('DROP_COMMAND'), 'Heavy breastplate', 'some container'])
		output = self.rpgJSON._runAction()
		self.assertTrue(output == {"error": {"message": _('ERROR_UNKNOWN_ITEM_CONTAINER_TYPE_LABEL'), "code": 1}})

	def test_not_available_container_type_text(self):
		self.rpgText.setAction([_('TAKE_COMMAND'), 'Heavy breastplate'])
		self.rpgText._runAction()
		self.rpgText.setAction([_('DROP_COMMAND'), 'Heavy breastplate', 'box'])
		output = self.rpgText._runAction()
		self.assertTrue(output == _('ERROR_CONTAINER_NOT_AVAILABLE'))

	def test_not_available_container_type_json(self):
		self.rpgJSON.setAction([_('TAKE_COMMAND'), 'Heavy breastplate'])
		self.rpgJSON._runAction()
		self.rpgJSON.setAction([_('DROP_COMMAND'), 'Heavy breastplate', 'box'])
		output = self.rpgJSON._runAction()
		self.assertTrue(output == {"error": {"message": _('ERROR_CONTAINER_NOT_AVAILABLE'), "code": 1}})

	# Container index tests
	def test_missing_container_index_text(self):
		self.rpgText.setAction([_('TAKE_COMMAND'), 'Heavy breastplate'])
		self.rpgText._runAction()
		self.rpgText.setAction([_('DROP_COMMAND'), 'Heavy breastplate', 'wardrobe'])
		output = self.rpgText._runAction()
		self.assertTrue(output == _('ERROR_MULTIPLE_CONTAINERS_AVAILABLE'))

	def test_missing_container_index_json(self):
		self.rpgJSON.setAction([_('TAKE_COMMAND'), 'Heavy breastplate'])
		self.rpgJSON._runAction()
		self.rpgJSON.setAction([_('DROP_COMMAND'), 'Heavy breastplate', 'wardrobe'])
		output = self.rpgJSON._runAction()
		self.assertTrue(output == {"error": {"message": _('ERROR_MULTIPLE_CONTAINERS_AVAILABLE'), "code": 1}})

	def test_invalid_container_index_text(self):
		self.rpgText.setAction([_('TAKE_COMMAND'), 'Heavy breastplate'])
		self.rpgText._runAction()
		self.rpgText.setAction([_('DROP_COMMAND'), 'Heavy breastplate', 'wardrobe', 'some index'])
		output = self.rpgText._runAction()
		self.assertTrue(output == _('ERROR_DROP_INVALID_CONTAINER_INDEX'))

	def test_invalid_container_index_json(self):
		self.rpgJSON.setAction([_('TAKE_COMMAND'), 'Heavy breastplate'])
		self.rpgJSON._runAction()
		self.rpgJSON.setAction([_('DROP_COMMAND'), 'Heavy breastplate', 'wardrobe', 'some index'])
		output = self.rpgJSON._runAction()
		self.assertTrue(output == {"error": {"message": _('ERROR_DROP_INVALID_CONTAINER_INDEX'), "code": 1}})

	def test_out_of_range_container_index_text(self):
		self.rpgText.setAction([_('TAKE_COMMAND'), 'Heavy breastplate'])
		self.rpgText._runAction()
		self.rpgText.setAction([_('DROP_COMMAND'), 'Heavy breastplate', 'wardrobe', 0])
		output = self.rpgText._runAction()
		self.assertTrue(output == _('ERROR_OUT_OF_RANGE_ITEM_CONTAINER_INDEX'))
		self.rpgText.setAction([_('DROP_COMMAND'), 'Heavy breastplate', 'wardrobe', 3])
		output = self.rpgText._runAction()
		self.assertTrue(output == _('ERROR_OUT_OF_RANGE_ITEM_CONTAINER_INDEX'))

	def test_out_of_range_container_index_json(self):
		self.rpgJSON.setAction([_('TAKE_COMMAND'), 'Heavy breastplate'])
		self.rpgJSON._runAction()
		self.rpgJSON.setAction([_('DROP_COMMAND'), 'Heavy breastplate', 'wardrobe', 0])
		output = self.rpgJSON._runAction()
		self.assertTrue(output == {"error": {"message": _('ERROR_OUT_OF_RANGE_ITEM_CONTAINER_INDEX'), "code": 1}})
		self.rpgJSON.setAction([_('DROP_COMMAND'), 'Heavy breastplate', 'wardrobe', 3])
		output = self.rpgJSON._runAction()
		self.assertTrue(output == {"error": {"message": _('ERROR_OUT_OF_RANGE_ITEM_CONTAINER_INDEX'), "code": 1}})

	# Tests OK
	def test_item_text(self):
		self.rpgText.setAction([_('TAKE_COMMAND'), 'Heavy breastplate'])
		self.rpgText._runAction()
		self.rpgText.setAction([_('DROP_COMMAND'), 'Heavy breastplate'])
		output = self.rpgText._runAction()
		self.assertTrue(output == _('DROP_CONFIRMATION_%(quantity)s_%(name)s') % {'quantity': 1, 'name': 'Heavy breastplate'})

	def test_item_json(self):
		self.rpgJSON.setAction([_('TAKE_COMMAND'), 'Heavy breastplate'])
		self.rpgJSON._runAction()
		self.rpgJSON.setAction([_('DROP_COMMAND'), 'Heavy breastplate'])
		output = self.rpgJSON._runAction()
		self.assertTrue(output == {"name": "Heavy breastplate", "quantity": 1})

	def test_item_container_text(self):
		self.rpgText.setAction([_('TAKE_COMMAND'), 'Heavy breastplate'])
		self.rpgText._runAction()
		self.rpgText.setAction([_('DROP_COMMAND'), 'Heavy breastplate', 'chest'])
		output = self.rpgText._runAction()
		self.assertTrue(output == _('DROP_CONFIRMATION_%(quantity)s_%(name)s') % {'quantity': 1, 'name': 'Heavy breastplate'})

	def test_item_container_json(self):
		self.rpgJSON.setAction([_('TAKE_COMMAND'), 'Heavy breastplate'])
		self.rpgJSON._runAction()
		self.rpgJSON.setAction([_('DROP_COMMAND'), 'Heavy breastplate', 'chest'])
		output = self.rpgJSON._runAction()
		self.assertTrue(output == {"name": "Heavy breastplate", "quantity": 1})

	def test_item_container_index_text(self):
		self.rpgText.setAction([_('TAKE_COMMAND'), 'Heavy breastplate'])
		self.rpgText._runAction()
		self.rpgText.setAction([_('DROP_COMMAND'), 'Heavy breastplate', 'wardrobe', 1])
		output = self.rpgText._runAction()
		self.assertTrue(output == _('DROP_CONFIRMATION_%(quantity)s_%(name)s') % {'quantity': 1, 'name': 'Heavy breastplate'})

	def test_item_container_index_json(self):
		self.rpgJSON.setAction([_('TAKE_COMMAND'), 'Heavy breastplate'])
		self.rpgJSON._runAction()
		self.rpgJSON.setAction([_('DROP_COMMAND'), 'Heavy breastplate', 'wardrobe', 1])
		output = self.rpgJSON._runAction()
		self.assertTrue(output == {"name": "Heavy breastplate", "quantity": 1})

	def test_quantity_item_text(self):
		self.rpgText.setAction([_('TAKE_COMMAND'), 2, 'Heavy breastplate'])
		self.rpgText._runAction()
		self.rpgText.setAction([_('DROP_COMMAND'), 2, 'Heavy breastplate'])
		output = self.rpgText._runAction()
		self.assertTrue(output == _('DROP_CONFIRMATION_%(quantity)s_%(name)s') % {'quantity': 2, 'name': 'Heavy breastplate'})

	def test_quantity_item_json(self):
		self.rpgJSON.setAction([_('TAKE_COMMAND'), 2, 'Heavy breastplate'])
		self.rpgJSON._runAction()
		self.rpgJSON.setAction([_('DROP_COMMAND'), 2, 'Heavy breastplate'])
		output = self.rpgJSON._runAction()
		self.assertTrue(output == {"name": "Heavy breastplate", "quantity": 2})

	def test_quantity_item_container_text(self):
		self.rpgText.setAction([_('TAKE_COMMAND'), 2, 'Heavy breastplate'])
		self.rpgText._runAction()
		self.rpgText.setAction([_('DROP_COMMAND'), 2, 'Heavy breastplate', 'chest'])
		output = self.rpgText._runAction()
		self.assertTrue(output == _('DROP_CONFIRMATION_%(quantity)s_%(name)s') % {'quantity': 2, 'name': 'Heavy breastplate'})

	def test_quantity_item_container_json(self):
		self.rpgJSON.setAction([_('TAKE_COMMAND'), 2, 'Heavy breastplate'])
		self.rpgJSON._runAction()
		self.rpgJSON.setAction([_('DROP_COMMAND'), 2, 'Heavy breastplate', 'chest'])
		output = self.rpgJSON._runAction()
		self.assertTrue(output == {"name": "Heavy breastplate", "quantity": 2})

	def test_quantity_item_container_index_text(self):
		self.rpgText.setAction([_('TAKE_COMMAND'), 2, 'Heavy breastplate'])
		self.rpgText._runAction()
		self.rpgText.setAction([_('DROP_COMMAND'), 2, 'Heavy breastplate', 'wardrobe', 1])
		output = self.rpgText._runAction()
		self.assertTrue(output == _('DROP_CONFIRMATION_%(quantity)s_%(name)s') % {'quantity': 2, 'name': 'Heavy breastplate'})

	def test_quantity_item_container_index_json(self):
		self.rpgJSON.setAction([_('TAKE_COMMAND'), 2, 'Heavy breastplate'])
		self.rpgJSON._runAction()
		self.rpgJSON.setAction([_('DROP_COMMAND'), 2, 'Heavy breastplate', 'wardrobe', 1])
		output = self.rpgJSON._runAction()
		self.assertTrue(output == {"name": "Heavy breastplate", "quantity": 2})
