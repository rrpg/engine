# -*- coding: utf-8 -*-
import unittest

import tests.common
from core.localisation import _
import json


class quitTests(tests.common.common):
	def test_no_place_given_text(self):
		self.rpg.setAction([_('QUIT_COMMAND')])
		output = self.rpg._runAction()
		self.assertEquals(output, -1)

	def test_no_place_given_json(self):
		self.rpg.setAction([_('QUIT_COMMAND')])
		output = self.rpg._runAction(True)
		self.assertEquals(output, -1)
