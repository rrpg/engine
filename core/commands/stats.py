# -*- coding: utf-8 -*-

from models import item
import core.command


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
		longestStat = max({len(stat): stat for stat in data.keys()})
		for i in data:
			output.append('{0}{1}'.format(i.upper().ljust(longestStat + 3), str(data[i]).rjust(4)))

		return '\n'.join(output)
