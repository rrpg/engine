# -*- coding: utf-8 -*-
import unittest

import tests.common
from core.localisation import _
import fake_model
import json


class fakeModeTests(tests.common.common):
	def setUp(self):
		super(fakeModeTests, self).setUp()
		fake_model.model.setDB(self.dbFile)

	def test_load_all(self):
		values = fake_model.model.loadAll()
		expected = [
			{'id': 1, 'field1': 3, 'field2': 'three'},
			{'id': 2, 'field1': 42, 'field2': 'forty-two'}
		]
		self.assertEquals(values, expected)

	def test_load_all_aliases(self):
		values = fake_model.model.loadAll(
			{'value': 'field1', 'name': 'field2'}
		)
		expected = [
			{'value': 3, 'name': 'three'},
			{'value': 42, 'name': 'forty-two'}
		]
		self.assertEquals(values, expected)

	def test_db(self):
		self.assertEquals(fake_model.model.getDB(), self.dbFile)
		fake_model.model.setDB('foo/bar')
		self.assertEquals(fake_model.model.getDB(), 'foo/bar')

	def test_bad_fields_format(self):
		with self.assertRaises(TypeError) as raised:
			fake_model.model.prepareFieldsForSelect(42)
		self.assertEquals(str(raised.exception), 'Unexpected type of fields (%s)' % type(42))
		with self.assertRaises(TypeError) as raised:
			fake_model.model.prepareFieldsForSelect(object)
		self.assertEquals(str(raised.exception), 'Unexpected type of fields (%s)' % type(object))
