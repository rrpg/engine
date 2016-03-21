# -*- coding: utf-8 -*-
import unittest

import tests.common
from core.localisation import _
import json


class listGendersTests(tests.common.common):
	login = None

	def test_text(self):
		self.rpgText.setAction(['list-genders'])
		output = self.rpgText._runAction()
		self.assertEquals(
			output, '\n'.join(['  0 - male', '  1 - female'])
		)

	def test_json(self):
		self.rpgJSON.setAction(['list-genders'])
		output = self.rpgJSON._runAction()
		self.assertEquals(output, [{'id': 1, 'name': 'male'}, {'id': 2, 'name': 'female'}])
