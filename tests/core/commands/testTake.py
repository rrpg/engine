# -*- coding: utf-8 -*-
import unittest

import tests.common
from core.localisation import _
import json


class takeTests(tests.common.common):
	# Quantity tests
	def test_invalid_quantity_text(self):
		self.rpg.setAction([_('TAKE_COMMAND'), 'ten', 'Heavy breastplate', 'chest', 1])
		output = self.rpg._runAction()
		self.assertEquals(output, _('ERROR_TAKE_INVALID_FORMAT_QUANTITY'))

	def test_invalid_quantity_json(self):
		self.rpg.setAction([_('TAKE_COMMAND'), 'ten', 'Heavy breastplate', 'chest', 1])
		output = self.rpg._runAction(True)
		self.assertEquals(output, {"error": {"message": _('ERROR_TAKE_INVALID_FORMAT_QUANTITY'), "code": 1}})

	def test_quantity_too_low_text(self):
		self.rpg.setAction([_('TAKE_COMMAND'), 0, 'Heavy breastplate'])
		output = self.rpg._runAction()
		self.assertEquals(output, _('ERROR_TAKE_TOO_LOW_QUANTITY'))

	def test_quantity_too_low_json(self):
		self.rpg.setAction([_('TAKE_COMMAND'), 0, 'Heavy breastplate'])
		output = self.rpg._runAction(True)
		self.assertEquals(output, {"error": {"message": _('ERROR_TAKE_TOO_LOW_QUANTITY'), "code": 1}})

	def test_quantity_too_high_text(self):
		self.rpg.setAction([_('TAKE_COMMAND'), 10, 'Heavy breastplate'])
		output = self.rpg._runAction()
		self.assertEquals(output, _('ERROR_TAKE_QUANTITY_TOO_HIGH_%s') % 'Heavy breastplate')

	def test_quantity_too_high_json(self):
		self.rpg.setAction([_('TAKE_COMMAND'), 10, 'Heavy breastplate'])
		output = self.rpg._runAction(True)
		self.assertEquals(output, {"error": {"message": _('ERROR_TAKE_QUANTITY_TOO_HIGH_%s') % 'Heavy breastplate', "code": 1}})

	# Items tests
	def test_item_missing_text(self):
		self.rpg.setAction([_('TAKE_COMMAND')])
		output = self.rpg._runAction()
		self.assertEquals(output, _('ERROR_TAKE_NO_ITEM_GIVEN'))

	def test_item_missing_json(self):
		self.rpg.setAction([_('TAKE_COMMAND')])
		output = self.rpg._runAction(True)
		self.assertEquals(output, {"error": {"message": _('ERROR_TAKE_NO_ITEM_GIVEN'), "code": 1}})

	def test_item_missing_with_quantity_text(self):
		self.rpg.setAction([_('TAKE_COMMAND'), 1])
		output = self.rpg._runAction()
		self.assertEquals(output, _('ERROR_TAKE_NO_ITEM_GIVEN'))

	def test_item_missing_with_quantity_json(self):
		self.rpg.setAction([_('TAKE_COMMAND'), 1])
		output = self.rpg._runAction(True)
		self.assertEquals(output, {"error": {"message": _('ERROR_TAKE_NO_ITEM_GIVEN'), "code": 1}})

	def test_unknown_item_text(self):
		self.rpg.setAction([_('TAKE_COMMAND'), 'some dummy item'])
		output = self.rpg._runAction()
		self.assertEquals(output, _('ERROR_TAKE_UNKNOWN_ITEM'))

	def test_unknown_item_json(self):
		self.rpg.setAction([_('TAKE_COMMAND'), 'some dummy item'])
		output = self.rpg._runAction(True)
		self.assertEquals(output, {"error": {"message": _('ERROR_TAKE_UNKNOWN_ITEM'), "code": 1}})

	def test_not_available_item_text(self):
		self.rpg.setAction([_('TAKE_COMMAND'), 'Mist potion'])
		output = self.rpg._runAction()
		self.assertEquals(output, _('ERROR_TAKE_ITEM_NOT_AVAILABLE'))

	def test_not_available_item_json(self):
		self.rpg.setAction([_('TAKE_COMMAND'), 'Mist potion'])
		output = self.rpg._runAction(True)
		self.assertEquals(output, {"error": {"message": _('ERROR_TAKE_ITEM_NOT_AVAILABLE'), "code": 1}})

	# Container tests
	def test_unknown_container_type_text(self):
		self.rpg.setAction([_('TAKE_COMMAND'), 'Heavy breastplate', 'some container'])
		output = self.rpg._runAction()
		self.assertEquals(output, _('ERROR_UNKNOWN_ITEM_CONTAINER_TYPE_LABEL'))

	def test_unknown_container_type_json(self):
		self.rpg.setAction([_('TAKE_COMMAND'), 'Heavy breastplate', 'some container'])
		output = self.rpg._runAction(True)
		self.assertEquals(output, {"error": {"message": _('ERROR_UNKNOWN_ITEM_CONTAINER_TYPE_LABEL'), "code": 1}})

	def test_not_available_container_type_text(self):
		self.rpg.setAction([_('TAKE_COMMAND'), 'Heavy breastplate', 'box'])
		output = self.rpg._runAction()
		self.assertEquals(output, _('ERROR_CONTAINER_NOT_AVAILABLE'))

	def test_not_available_container_type_json(self):
		self.rpg.setAction([_('TAKE_COMMAND'), 'Heavy breastplate', 'box'])
		output = self.rpg._runAction(True)
		self.assertEquals(output, {"error": {"message": _('ERROR_CONTAINER_NOT_AVAILABLE'), "code": 1}})

	# Container index tests
	def test_missing_container_index_text(self):
		self.rpg.setAction([_('TAKE_COMMAND'), 'Heavy breastplate', 'wardrobe'])
		output = self.rpg._runAction()
		self.assertEquals(output, _('ERROR_MULTIPLE_CONTAINERS_AVAILABLE'))

	def test_missing_container_index_json(self):
		self.rpg.setAction([_('TAKE_COMMAND'), 'Heavy breastplate', 'wardrobe'])
		output = self.rpg._runAction(True)
		self.assertEquals(output, {"error": {"message": _('ERROR_MULTIPLE_CONTAINERS_AVAILABLE'), "code": 1}})

	def test_invalid_container_index_text(self):
		self.rpg.setAction([_('TAKE_COMMAND'), 'Heavy breastplate', 'wardrobe', 'some index'])
		output = self.rpg._runAction()
		self.assertEquals(output, _('ERROR_TAKE_INVALID_CONTAINER_INDEX'))

	def test_invalid_container_index_json(self):
		self.rpg.setAction([_('TAKE_COMMAND'), 'Heavy breastplate', 'wardrobe', 'some index'])
		output = self.rpg._runAction(True)
		self.assertEquals(output, {"error": {"message": _('ERROR_TAKE_INVALID_CONTAINER_INDEX'), "code": 1}})

	def test_out_of_range_container_index_text(self):
		self.rpg.setAction([_('TAKE_COMMAND'), 'Heavy breastplate', 'wardrobe', 0])
		output = self.rpg._runAction()
		self.assertEquals(output, _('ERROR_OUT_OF_RANGE_ITEM_CONTAINER_INDEX_%d') % (2,))
		self.rpg.setAction([_('TAKE_COMMAND'), 'Heavy breastplate', 'wardrobe', 3])
		output = self.rpg._runAction()
		self.assertEquals(output, _('ERROR_OUT_OF_RANGE_ITEM_CONTAINER_INDEX_%d') % (2,))

	def test_out_of_range_container_index_json(self):
		self.rpg.setAction([_('TAKE_COMMAND'), 'Heavy breastplate'])
		self.rpg._runAction(True)
		self.rpg.setAction([_('TAKE_COMMAND'), 'Heavy breastplate', 'wardrobe', 0])
		output = self.rpg._runAction(True)
		self.assertEquals(output, {"error": {"message": _('ERROR_OUT_OF_RANGE_ITEM_CONTAINER_INDEX_%d') % (2,), "code": 1}})
		self.rpg.setAction([_('TAKE_COMMAND'), 'Heavy breastplate', 'wardrobe', 3])
		output = self.rpg._runAction(True)
		self.assertEquals(output, {"error": {"message": _('ERROR_OUT_OF_RANGE_ITEM_CONTAINER_INDEX_%d') % (2,), "code": 1}})

	# Tests OK
	def test_item_text(self):
		self.rpg.setAction([_('TAKE_COMMAND'), 'Heavy breastplate'])
		output = self.rpg._runAction()
		self.assertEquals(output, _('TAKE_CONFIRMATION_%(quantity)s_%(name)s') % {'quantity': 1, 'name': 'Heavy breastplate'})
		self.rpg.setAction([_('LOOK_COMMAND'), _('LOOK_OBJECTS_PARAM')])
		output = self.rpg._runAction()
		self.assertEquals(output, _('AVAILABLE_ITEMS') +'\n'+\
			'  5 Heavy breastplate')

	def test_item_json(self):
		self.rpg.setAction([_('TAKE_COMMAND'), 'Heavy breastplate'])
		output = self.rpg._runAction(True)
		self.assertEquals(output, {"name": "Heavy breastplate", "quantity": 1})

	def test_item_container_text(self):
		self.rpg.setAction([_('TAKE_COMMAND'), 'Heavy breastplate', 'chest'])
		output = self.rpg._runAction()
		self.assertEquals(output, _('TAKE_CONFIRMATION_%(quantity)s_%(name)s') % {'quantity': 1, 'name': 'Heavy breastplate'})

	def test_item_container_json(self):
		self.rpg.setAction([_('TAKE_COMMAND'), 'Heavy breastplate', 'chest'])
		output = self.rpg._runAction(True)
		self.assertEquals(output, {"name": "Heavy breastplate", "quantity": 1})

	def test_item_container_index_text(self):
		self.rpg.setAction([_('TAKE_COMMAND'), 'Heavy breastplate', 'wardrobe', 1])
		output = self.rpg._runAction()
		self.assertEquals(output, _('TAKE_CONFIRMATION_%(quantity)s_%(name)s') % {'quantity': 1, 'name': 'Heavy breastplate'})

	def test_item_container_index_json(self):
		self.rpg.setAction([_('TAKE_COMMAND'), 'Heavy breastplate', 'wardrobe', 1])
		output = self.rpg._runAction(True)
		self.assertEquals(output, {"name": "Heavy breastplate", "quantity": 1})

	def test_quantity_item_text(self):
		self.rpg.setAction([_('TAKE_COMMAND'), 2, 'Heavy breastplate'])
		output = self.rpg._runAction()
		self.assertEquals(output, _('TAKE_CONFIRMATION_%(quantity)s_%(name)s') % {'quantity': 2, 'name': 'Heavy breastplate'})

	def test_quantity_item_json(self):
		self.rpg.setAction([_('TAKE_COMMAND'), 2, 'Heavy breastplate'])
		output = self.rpg._runAction(True)
		self.assertEquals(output, {"name": "Heavy breastplate", "quantity": 2})

	def test_quantity_item_container_text(self):
		self.rpg.setAction([_('TAKE_COMMAND'), 2, 'Heavy breastplate', 'chest'])
		output = self.rpg._runAction()
		self.assertEquals(output, _('TAKE_CONFIRMATION_%(quantity)s_%(name)s') % {'quantity': 2, 'name': 'Heavy breastplate'})

	def test_quantity_item_container_json(self):
		self.rpg.setAction([_('TAKE_COMMAND'), 2, 'Heavy breastplate', 'chest'])
		output = self.rpg._runAction(True)
		self.assertEquals(output, {"name": "Heavy breastplate", "quantity": 2})

	def test_quantity_item_container_index_text(self):
		self.rpg.setAction([_('TAKE_COMMAND'), 2, 'Heavy breastplate', 'wardrobe', 1])
		output = self.rpg._runAction()
		self.assertEquals(output, _('TAKE_CONFIRMATION_%(quantity)s_%(name)s') % {'quantity': 2, 'name': 'Heavy breastplate'})

	def test_quantity_item_container_index_json(self):
		self.rpg.setAction([_('TAKE_COMMAND'), 2, 'Heavy breastplate', 'wardrobe', 1])
		output = self.rpg._runAction(True)
		self.assertEquals(output, {"name": "Heavy breastplate", "quantity": 2})
