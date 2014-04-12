# -*- coding: utf-8 -*-

import core.command
from core import utils
import getpass
from core.localisation import _
from models import player, gender, species

class listSpecies(core.command.command):
	def run(self):
		"""
		c.run()

		If the command is run as a stand alone command, the player informations
		must be provided. If it is not run as a stand alone command, the
		informations will be read from stdin
		"""

		sps = species.model.getSpecies()
		return [{
			'id': s['id_species'],
			'name': s['name'],
			'description': s['description']
			} for s in sps]

	def render(self, data):
		ret = list()
		for k, v in enumerate(data):
			ret.append(str(k).rjust(3) + ' - ' + v['name'])
			ret.append(v['description'])
		return '\n'.join(ret)
