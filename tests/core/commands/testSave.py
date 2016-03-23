# -*- coding: utf-8 -*-
import unittest

import tests.common
from core.localisation import _
import json


class moveTests(tests.common.common):
	# test item in area
	# test item in container
	# test item in inventory
	# test player position
	# test player inventory
	# test player stats

	def test_save_no_change_text(self):
		self.rpg.setAction([_('SAVE_COMMAND')])
		self.rpg._runAction()

		self.initialiseClient()

		self.rpg.setAction([_('INVENTORY_COMMAND')])
		output = self.rpg._runAction()
		self.assertEquals(output, _('INVENTORY_EMPTY'))

	def test_save_no_change_json(self):
		self.rpg.setAction([_('SAVE_COMMAND')])
		self.rpg._runAction(True)

		self.initialiseClient()

		self.rpg.setAction([_('INVENTORY_COMMAND')])
		output = self.rpg._runAction(True)
		self.assertEquals(output, [])

	def test_no_save_take_text(self):
		# do a change
		# restart engine
		# check the change, must not have been saved
		self.rpg.setAction([_('TAKE_COMMAND'), 'Heavy breastplate'])
		self.rpg._runAction()

		self.initialiseClient()

		self.rpg.setAction([_('INVENTORY_COMMAND')])
		output = self.rpg._runAction()
		self.assertEquals(output, _('INVENTORY_EMPTY'))
		self.rpg.setAction([_('LOOK_COMMAND'), _('LOOK_OBJECTS_PARAM')])
		output = self.rpg._runAction()
		self.assertEquals(output, _('AVAILABLE_ITEMS') +'\n'+\
			'  6 Heavy breastplate')

	def test_no_save_take_json(self):
		# do a change
		# restart engine
		# check the change, must not have been saved
		self.rpg.setAction([_('TAKE_COMMAND'), 'Heavy breastplate'])
		self.rpg._runAction(True)

		self.initialiseClient()

		self.rpg.setAction([_('INVENTORY_COMMAND')])
		output = self.rpg._runAction(True)
		self.assertEquals(output, [])
		self.rpg.setAction([_('LOOK_COMMAND'), _('LOOK_OBJECTS_PARAM')])
		output = self.rpg._runAction(True)
		self.assertEquals(output, {"items": [{"name": "Heavy breastplate", "quantity": 6}]})

	def test_save_take_text(self):
		# do a change
		# save
		# restart engine
		# check the change, must have been saved
		self.rpg.setAction([_('TAKE_COMMAND'), 'Heavy breastplate'])
		self.rpg._runAction()
		self.rpg.setAction([_('SAVE_COMMAND')])
		self.rpg._runAction()

		self.initialiseClient()

		self.rpg.setAction([_('INVENTORY_COMMAND')])
		output = self.rpg._runAction()
		self.assertEquals(output, '  1 Heavy breastplate')
		self.rpg.setAction([_('LOOK_COMMAND'), _('LOOK_OBJECTS_PARAM')])
		output = self.rpg._runAction()
		self.assertEquals(output, _('AVAILABLE_ITEMS') +'\n'+\
			'  5 Heavy breastplate')

	def test_save_take_json(self):
		# do a change
		# restart engine
		# check the change, must not have been saved
		self.rpg.setAction([_('TAKE_COMMAND'), 'Heavy breastplate'])
		self.rpg._runAction(True)
		self.rpg.setAction([_('SAVE_COMMAND')])
		self.rpg._runAction(True)

		self.initialiseClient()

		self.rpg.setAction([_('INVENTORY_COMMAND')])
		output = self.rpg._runAction(True)
		self.assertEquals(output, [{"name": "Heavy breastplate", "quantity": 1}])
		self.rpg.setAction([_('LOOK_COMMAND'), _('LOOK_OBJECTS_PARAM')])
		output = self.rpg._runAction(True)
		self.assertEquals(output, {"items": [{"name": "Heavy breastplate", "quantity": 5}]})

	def test_no_save_take_container_text(self):
		# do a change
		# restart engine
		# check the change, must not have been saved
		self.rpg.setAction([_('TAKE_COMMAND'), 'Heavy breastplate', 'chest'])
		self.rpg._runAction()

		self.initialiseClient()

		self.rpg.setAction([_('INVENTORY_COMMAND')])
		output = self.rpg._runAction()
		self.assertEquals(output, _('INVENTORY_EMPTY'))
		self.rpg.setAction([_('OPEN_COMMAND'), 'chest'])
		output = self.rpg._runAction()
		expected = [
			_('ITEMS_IN_CONTAINER_%s') % 'chest',
			'  4 Heavy breastplate'
		]
		self.assertEquals(output, '\n'.join(expected))

	def test_no_save_take_container_json(self):
		# do a change
		# restart engine
		# check the change, must not have been saved
		self.rpg.setAction([_('TAKE_COMMAND'), 'Heavy breastplate', 'chest'])
		self.rpg._runAction(True)

		self.initialiseClient()

		self.rpg.setAction([_('INVENTORY_COMMAND')])
		output = self.rpg._runAction(True)
		self.assertEquals(output, [])
		self.rpg.setAction([_('OPEN_COMMAND'), 'chest'])
		output = self.rpg._runAction(True)
		self.assertEquals(output, {'items': [{'name': 'Heavy breastplate', 'quantity': 4}], 'container_type': 'chest'})

	def test_save_take_container_text(self):
		# do a change
		# save
		# restart engine
		# check the change, must have been saved
		self.rpg.setAction([_('TAKE_COMMAND'), 'Heavy breastplate', 'chest'])
		self.rpg._runAction()
		self.rpg.setAction([_('SAVE_COMMAND')])
		self.rpg._runAction()

		self.initialiseClient()

		self.rpg.setAction([_('INVENTORY_COMMAND')])
		output = self.rpg._runAction()
		self.assertEquals(output, '  1 Heavy breastplate')
		self.rpg.setAction([_('OPEN_COMMAND'), 'chest'])
		output = self.rpg._runAction()
		expected = [
			_('ITEMS_IN_CONTAINER_%s') % 'chest',
			'  3 Heavy breastplate'
		]
		self.assertEquals(output, '\n'.join(expected))

	def test_save_take_container_json(self):
		# do a change
		# restart engine
		# check the change, must not have been saved
		self.rpg.setAction([_('TAKE_COMMAND'), 'Heavy breastplate', 'chest'])
		self.rpg._runAction(True)
		self.rpg.setAction([_('SAVE_COMMAND')])
		self.rpg._runAction(True)

		self.initialiseClient()

		self.rpg.setAction([_('INVENTORY_COMMAND')])
		output = self.rpg._runAction(True)
		self.assertEquals(output, [{"name": "Heavy breastplate", "quantity": 1}])
		self.rpg.setAction([_('OPEN_COMMAND'), 'chest'])
		output = self.rpg._runAction(True)
		self.assertEquals(output, {'items': [{'name': 'Heavy breastplate', 'quantity': 3}], 'container_type': 'chest'})

	def test_no_save_move_json(self):
		self.rpg.setAction([_('MOVE_COMMAND'), _('DIRECTION_KEY_SOUTH')])
		outputMove = self.rpg._runAction(True)

		self.initialiseClient()

		self.rpg.setAction([_('LOOK_COMMAND'), _('LOOK_REGION_PARAM')])
		outputLook = self.rpg._runAction(True)
		self.assertNotEquals((outputMove['x'], outputMove['y']), (outputLook['region']['x'], outputLook['region']['y']))

	def test_save_move_json(self):
		self.rpg.setAction([_('MOVE_COMMAND'), _('DIRECTION_KEY_SOUTH')])
		outputMove = self.rpg._runAction(True)
		self.rpg.setAction([_('SAVE_COMMAND')])
		self.rpg._runAction(True)

		self.initialiseClient()

		self.rpg.setAction([_('LOOK_COMMAND'), _('LOOK_REGION_PARAM')])
		outputLook = self.rpg._runAction(True)
		self.assertEquals((outputMove['x'], outputMove['y']), (outputLook['region']['x'], outputLook['region']['y']))

	def test_no_save_point_json(self):
		self.rpg.setAction([_('MOVE_COMMAND'), _('DIRECTION_KEY_SOUTH')])
		outputMove = self.rpg._runAction(True)
		self.rpg.setAction([_('MOVE_COMMAND'), _('DIRECTION_KEY_SOUTH')])
		outputMove = self.rpg._runAction(True)
		self.rpg.setAction([_('TAKE_COMMAND'), 'Heavy breastplate'])
		self.rpg._runAction(True)
		self.rpg.setAction([_('SAVE_COMMAND')])
		outputSave = self.rpg._runAction(True)
		self.assertEquals(outputSave, {'error': {'message': _('ERROR_SAVE_NO_SAVE_POINT'), 'code': 1}})

		self.initialiseClient()

		self.rpg.setAction([_('INVENTORY_COMMAND')])
		output = self.rpg._runAction(True)
		self.assertEquals(output, [])
		self.rpg.setAction([_('LOOK_COMMAND'), _('LOOK_OBJECTS_PARAM')])
		output = self.rpg._runAction(True)
		self.assertEquals(output, {"items": [{"name": "Heavy breastplate", "quantity": 6}]})
		self.rpg.setAction([_('LOOK_COMMAND'), _('LOOK_REGION_PARAM')])
		outputLook = self.rpg._runAction(True)
		self.assertNotEquals((outputMove['x'], outputMove['y']), (outputLook['region']['x'], outputLook['region']['y']))
