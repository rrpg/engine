# -*- coding: utf-8 -*-
import unittest
import sys
import os
sys.path.append(os.path.realpath(__file__ + "/../../../"))

import tests.common
from core.localisation import _
import json


class listSpeciesTests(tests.common.common):
	login = None
	password = None

	def test_text(self):
		self.rpgText.setAction(['list-species'])
		output = self.rpgText._runAction()
		self.assertTrue(
			output == '\n'.join(['  0 - Human', 'Humans come from planet Earth'])
		)

	def test_json(self):
		self.rpgJSON.setAction(['list-species'])
		output = self.rpgJSON._runAction()
		self.assertTrue(output == [{'description': 'Humans come from planet Earth', 'id': 1, 'name': 'Human'}])
