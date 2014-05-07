# -*- coding: utf-8 -*-
import unittest
import sys
import os
sys.path.append(os.path.realpath(__file__ + "/../../../"))

import tests.common
from core.localisation import _
import json


'''
possible cases:

drop
	ERROR_DROP_NO_ITEM_GIVEN
drop obj
	OK
	ERROR_DROP_UNKNOWN_ITEM
	ERROR_DROP_ITEM_NOT_AVAILABLE

drop obj container
	OK
	ERROR_DROP_UNKNOWN_ITEM
	ERROR_DROP_ITEM_NOT_AVAILABLE (not in inventory)
	ERROR_UNKNOWN_CONTAINER
	ERROR_CONTAINER_NOT_AVAILABLE

drop obj container index
	OK
	ERROR_DROP_UNKNOWN_ITEM
	ERROR_DROP_ITEM_NOT_AVAILABLE (not in inventory)
	ERROR_UNKNOWN_CONTAINER
	ERROR_CONTAINER_NOT_AVAILABLE
	ERROR_INVALID_CONTAINER_INDEX
	ERROR_CONTAINER_INDEX_NOT_AVAILABLE

drop quantity
	ERROR_DROP_NO_ITEM_GIVEN
drop quantity obj
	OK
	ERROR_DROP_UNKNOWN_ITEM
	ERROR_DROP_ITEM_NOT_AVAILABLE
	ERROR_INVALID_QUANTITY
	ERROR_QUANTITY_TOO_HIGH

drop quantity obj container
	OK
	ERROR_DROP_UNKNOWN_ITEM
	ERROR_DROP_ITEM_NOT_AVAILABLE (not in inventory)
	ERROR_UNKNOWN_CONTAINER
	ERROR_CONTAINER_NOT_AVAILABLE
	ERROR_INVALID_QUANTITY
	ERROR_QUANTITY_TOO_HIGH

drop quantity obj container index
	OK
	ERROR_DROP_UNKNOWN_ITEM
	ERROR_DROP_ITEM_NOT_AVAILABLE (not in inventory)
	ERROR_UNKNOWN_CONTAINER
	ERROR_CONTAINER_NOT_AVAILABLE
	ERROR_INVALID_CONTAINER_INDEX
	ERROR_CONTAINER_INDEX_NOT_AVAILABLE
	ERROR_INVALID_QUANTITY
	ERROR_WRONG_FORMAT_QUANTITY
	ERROR_QUANTITY_TOO_HIGH

'''


class dropTests(tests.common.common):
	def test_no_arg_text(self):
		self.rpgText.setAction([_('DROP_COMMAND')])
		output = self.rpgText._runAction()
		self.assertTrue(output == _('ERROR_DROP_NO_ITEM_GIVEN'))

	def test_no_arg_json(self):
		self.rpgJSON.setAction([_('DROP_COMMAND')])
		output = self.rpgJSON._runAction()
		self.assertTrue(output == {"error": {"message": _('ERROR_DROP_NO_ITEM_GIVEN'), "code": 1}})

	def test_item_text(self):
		self.rpgText.setAction([_('DROP_COMMAND'), 'some dummy item'])
		output = self.rpgText._runAction()
		self.assertTrue(output == _('ERROR_DROP_UNKNOWN_ITEM'))

		self.rpgText.setAction([_('DROP_COMMAND'), 'Mist potion'])
		output = self.rpgText._runAction()
		self.assertTrue(output == _('ERROR_DROP_ITEM_NOT_AVAILABLE'))

		self.rpgText.setAction([_('TAKE_COMMAND'), 'Heavy breastplate'])
		self.rpgText._runAction()
		self.rpgText.setAction([_('DROP_COMMAND'), 'Heavy breastplate'])
		output = self.rpgText._runAction()
		self.assertTrue(output == _('DROP_CONFIRMATION_%(quantity)s_%(name)s') % {'quantity': 1, 'name': 'Heavy breastplate'})

	def test_item_json(self):
		self.rpgJSON.setAction([_('DROP_COMMAND'), 'some dummy item'])
		output = self.rpgJSON._runAction()
		self.assertTrue(output == {"error": {"message": _('ERROR_DROP_UNKNOWN_ITEM'), "code": 1}})

		self.rpgJSON.setAction([_('DROP_COMMAND'), 'Mist potion'])
		output = self.rpgJSON._runAction()
		self.assertTrue(output == {"error": {"message": _('ERROR_DROP_ITEM_NOT_AVAILABLE'), "code": 1}})

		self.rpgJSON.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER')
		self.rpgJSON.setAction([_('TAKE_COMMAND'), 'Heavy breastplate'])
		self.rpgJSON._runAction()
		self.rpgJSON.setAction([_('DROP_COMMAND'), 'Heavy breastplate'])
		output = self.rpgJSON._runAction()
		self.assertTrue(output == {"name": "Heavy breastplate", "quantity": 1})

	def test_item_container_text(self):
		self.rpgText.setAction([_('DROP_COMMAND'), 'some dummy item', 'chest'])
		output = self.rpgText._runAction()
		self.assertTrue(output == _('ERROR_DROP_UNKNOWN_ITEM'))

		self.rpgText.setAction([_('DROP_COMMAND'), 'Mist potion', 'chest'])
		output = self.rpgText._runAction()
		self.assertTrue(output == _('ERROR_DROP_ITEM_NOT_AVAILABLE'))

		self.rpgText.setAction([_('TAKE_COMMAND'), 'Heavy breastplate'])
		self.rpgText._runAction()

		self.rpgText.setAction([_('DROP_COMMAND'), 'Heavy breastplate', 'some container'])
		output = self.rpgText._runAction()
		self.assertTrue(output == _('ERROR_UNKNOWN_ITEM_CONTAINER_TYPE_LABEL'))

		self.rpgText.setAction([_('DROP_COMMAND'), 'Heavy breastplate', 'box'])
		output = self.rpgText._runAction()
		self.assertTrue(output == _('ERROR_CONTAINER_NOT_AVAILABLE'))

		self.rpgText.setAction([_('DROP_COMMAND'), 'Heavy breastplate', 'chest'])
		output = self.rpgText._runAction()
		self.assertTrue(output == _('DROP_CONFIRMATION_%(quantity)s_%(name)s') % {'quantity': 1, 'name': 'Heavy breastplate'})

	def test_item_container_json(self):
		self.rpgJSON.setAction([_('DROP_COMMAND'), 'some dummy item'])
		output = self.rpgJSON._runAction()
		self.assertTrue(output == {"error": {"message": _('ERROR_DROP_UNKNOWN_ITEM'), "code": 1}})

		self.rpgJSON.setAction([_('DROP_COMMAND'), 'Mist potion'])
		output = self.rpgJSON._runAction()
		self.assertTrue(output == {"error": {"message": _('ERROR_DROP_ITEM_NOT_AVAILABLE'), "code": 1}})

		self.rpgJSON.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER')
		self.rpgJSON.setAction([_('TAKE_COMMAND'), 'Heavy breastplate'])
		self.rpgJSON._runAction()

		self.rpgJSON.setAction([_('DROP_COMMAND'), 'Heavy breastplate', 'some container'])
		output = self.rpgJSON._runAction()
		self.assertTrue(output == {"error": {"message": _('ERROR_UNKNOWN_ITEM_CONTAINER_TYPE_LABEL'), "code": 1}})

		self.rpgJSON.setAction([_('DROP_COMMAND'), 'Heavy breastplate', 'box'])
		output = self.rpgJSON._runAction()
		self.assertTrue(output == {"error": {"message": _('ERROR_CONTAINER_NOT_AVAILABLE'), "code": 1}})

		self.rpgJSON.setAction([_('DROP_COMMAND'), 'Heavy breastplate'])
		output = self.rpgJSON._runAction()
		self.assertTrue(output == {"name": "Heavy breastplate", "quantity": 1})

	def test_item_container_index_text(self):
		pass

	def test_item_container_index_json(self):
		pass

	def test_quantity_text(self):
		pass

	def test_quantity_json(self):
		pass

	def test_quantity_item_text(self):
		pass

	def test_quantity_item_json(self):
		pass

	def test_quantity_item_container_text(self):
		pass

	def test_quantity_item_container_json(self):
		pass

	def test_quantity_item_container_index_text(self):
		pass

	def test_quantity_item_container_index_json(self):
		pass


	def test_no_item_given_text(self):
		self.rpgText.setAction([_('DROP_COMMAND')])
		output = self.rpgText._runAction()
		self.assertTrue(output == _('ERROR_DROP_NO_ITEM_GIVEN'))

	def test_no_item_given_json(self):
		self.rpgJSON.setAction([_('DROP_COMMAND')])
		output = self.rpgJSON._runAction()
		self.assertTrue(output == {"error": {"message": _('ERROR_DROP_NO_ITEM_GIVEN'), "code": 1}})

	def test_invalid_quantity_text(self):
		self.rpgText.setAction([_('DROP_COMMAND'), 'ten', 'Heavy breastplate', 'chest', 1])
		output = self.rpgText._runAction()
		self.assertTrue(output == _('ERROR_DROP_INVALID_QUANTITY'))

	def test_invalid_quantity_json(self):
		self.rpgJSON.setAction([_('DROP_COMMAND'), 'ten', 'Heavy breastplate', 'chest', 1])
		output = self.rpgJSON._runAction()
		self.assertTrue(output == {"error": {"message": _('ERROR_DROP_INVALID_QUANTITY'), "code": 1}})

	def test_quantity_too_high_text(self):
		self.rpgText.setAction([_('TAKE_COMMAND'), 2, 'Heavy breastplate'])
		self.rpgText._runAction()
		self.rpgText.setAction([_('DROP_COMMAND'), 10, 'Heavy breastplate'])
		output = self.rpgText._runAction()
		self.assertTrue(output == _('ERROR_DROP_QUANTITY_TOO_HIGH_%s') % 'Heavy breastplate')

	def test_quantity_too_high_json(self):
		self.rpgJSON.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER')
		self.rpgJSON.setAction([_('TAKE_COMMAND'), 2, 'Heavy breastplate'])
		self.rpgJSON._runAction()
		self.rpgJSON.setAction([_('DROP_COMMAND'), 10, 'Heavy breastplate'])
		output = self.rpgJSON._runAction()
		self.assertTrue(output == {"error": {"message": _('ERROR_DROP_QUANTITY_TOO_HIGH_%s') % 'Heavy breastplate', "code": 1}})

	def test_with_quantity_text(self):
		self.rpgText.setAction([_('TAKE_COMMAND'), 2, 'Heavy breastplate'])
		self.rpgText._runAction()
		self.rpgText.setAction([_('DROP_COMMAND'), 2, 'Heavy breastplate'])
		output = self.rpgText._runAction()
		self.assertTrue(output == _('DROP_CONFIRMATION_%(quantity)s_%(name)s') % {'quantity': 2, 'name': 'Heavy breastplate'})

	def test_with_quantity_json(self):
		self.rpgJSON.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER')
		self.rpgJSON.setAction([_('TAKE_COMMAND'), 2, 'Heavy breastplate'])
		self.rpgJSON._runAction()
		self.rpgJSON.setAction([_('DROP_COMMAND'), 2, 'Heavy breastplate'])
		output = self.rpgJSON._runAction()
		self.assertTrue(output == {"name": "Heavy breastplate", "quantity": 2})
