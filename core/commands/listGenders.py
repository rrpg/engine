# -*- coding: utf-8 -*-

import core.command
from core import utils
import getpass
from core.localisation import _
from models import player, gender, species

class listGenders(core.command.command):
	def run(self):
		"""
		c.run()

		If the command is run as a stand alone command, the player informations
		must be provided. If it is not run as a stand alone command, the
		informations will be read from stdin
		"""

		genders = gender.model.loadAll()
		return [{
			'id': g['id_gender'],
			'name': g['name']
			} for g in genders]

	def render(self, data):
		ret = list()
		for k, v in enumerate(data):
			ret.append(str(k).rjust(3) + ' - ' + v['name'])
		return '\n'.join(ret)
