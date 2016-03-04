# -*- coding: utf-8 -*-

from models import item
import core.command
from core.localisation import _


class stats(core.command.command):
	def run(self):
		"""
		c.run()

		Display the player's stats.
		"""
		return self._player.getStats()

	@staticmethod
	def formatStat(statLabel, labelLength, stat):
		return '{0}{1}'.format(
			statLabel.ljust(labelLength), stat
		)

	@staticmethod
	def padStat(stat, padding):
		return str(stat).rjust(padding)


	def render(self, data):
		output = list()
		statsLabels = {
			'stat_current_hp': _('STAT_CURRENT_HP'),
			'stat_max_hp': _('STAT_MAX_HP'),
			'stat_strength': _('STAT_STRENGTH'),
			'stat_defence': _('STAT_DEFENCE'),
			'stat_speed': _('STAT_SPEED'),
			'stat_accuracy': _('STAT_ACCURACY')
		}
		longestStat = max({len(stat): stat for stat in statsLabels.values()})

		for i in data:
			output.append(stats.formatStat(
				statsLabels[i],
				longestStat,
				stats.padStat(data[i], 4)
			))

		return '\n'.join(output)
