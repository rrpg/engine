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

	def render(self, data):
		output = list()
		longestStat = max({len(stat): stat for stat in data.keys()})
		for i in data:
			output.append('{0}{1}'.format(i.ljust(longestStat + 3), str(data[i]).rjust(4)))

		return '\n'.join(output)
