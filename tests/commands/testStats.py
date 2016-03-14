# -*- coding: utf-8 -*-
import unittest
import sys
import os
sys.path.append(os.path.realpath(__file__ + "/../../../"))

import tests.common
from core.localisation import _
import json
import re


class enterTests(tests.common.common):
	def test_empty_text(self):
		self.rpgText.setAction([_('STATS_COMMAND')])
		output = self.rpgText._runAction()
		stats = [
			_('STAT_CURRENT_HP'),
			_('STAT_DEFENCE'),
			_('STAT_ATTACK'),
			_('STAT_SPEED'),
			_('STAT_LUCK')
		]
		statsValues = ['20 / 20', '2', '4', '2', '10']
		output = output.split('\n')
		lineLength = None
		lineLengths = []
		for (i, l) in enumerate(output):
			matchObj = re.match('([^\s]+)\s+(\d{1,2}(?: / \d{1,2})?)', l)
			lineLength = len(l)
			lineLengths.append(len(l))
			self.assertEquals(matchObj.group(1), stats[i])
			self.assertEquals(matchObj.group(2), statsValues[i])

		self.assertEquals(lineLengths, [lineLength] * len(output))

	def test_empty_json(self):
		self.rpgJSON.setAction([_('STATS_COMMAND')])
		output = self.rpgJSON._runAction()
		expected = {
			'stat_current_hp': 20,
			'stat_max_hp': 20,
			'stat_defence': 2,
			'stat_attack': 4,
			'stat_speed': 2,
			'stat_luck': 10
		}
		self.assertEquals(output, expected)
