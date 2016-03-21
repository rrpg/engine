# -*- coding: utf-8 -*-
import unittest

import tests.common
from core.localisation import _
import models.settings
import json


class settingsTests(tests.common.common):
	def test_unknown_setting(self):
		thrownException = None
		try:
			models.settings.settings.get('foo')
		except IndexError as e:
			thrownException = str(e)

		self.assertEquals(thrownException, "Unknown key foo in the settings")

	def test_ok(self):
		s = models.settings.settings.get('START_CELL_ID')
		self.assertEquals(s, '1')
