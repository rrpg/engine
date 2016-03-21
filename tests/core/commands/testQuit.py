# -*- coding: utf-8 -*-
import unittest

import tests.common
from core.localisation import _
import json


class quitTests(tests.common.common):
	def test_no_place_given_text(self):
		self.rpgText.setAction([_('QUIT_COMMAND')])
		output = self.rpgText._runAction()
		self.assertEquals(output, -1)

	def test_no_place_given_json(self):
		self.rpgJSON.setAction([_('QUIT_COMMAND')])
		output = self.rpgJSON._runAction()
		self.assertEquals(output, -1)
