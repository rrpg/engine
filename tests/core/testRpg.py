# -*- coding: utf-8 -*-
import unittest

import tests.common
import core
from core.localisation import _
from core import Rpg
import models.settings
import json


class rpgTests(tests.common.common):
		def test_unknown_world(self):
			rpgEngine = Rpg.Rpg()
			try:
				rpgEngine.init("some/unexisting/world", "uselessLogin")
			except core.exception.exception as e:
				self.assertEquals(e.message, _('ERROR_UNKNOWN_SELECTED_WORLD'))
