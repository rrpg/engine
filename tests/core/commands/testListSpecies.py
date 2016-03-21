# -*- coding: utf-8 -*-
import unittest

import tests.common
from core.localisation import _
import json


class listSpeciesTests(tests.common.common):
	login = None

	def test_text(self):
		self.rpgText.setAction(['list-species'])
		output = self.rpgText._runAction()
		self.assertEquals(
			output, '\n'.join(['  0 - Human', 'Humans come from planet Earth'])
		)

	def test_json(self):
		self.rpgJSON.setAction(['list-species'])
		output = self.rpgJSON._runAction()
		self.assertEquals(output, [{'description': 'Humans come from planet Earth', 'id': 1, 'name': 'Human'}])
