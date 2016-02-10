# -*- coding: utf-8 -*-

import core.command
from core import utils
import getpass
from core.localisation import _
from models import player, gender, species

class createPlayer(core.command.command):
	def run(self):
		"""
		c.run()

		If the command is run as a stand alone command, the player informations
		must be provided. If it is not run as a stand alone command, the
		informations will be read from stdin
		"""

		if self._isInteractive: # pragma: no cover
			return self.interactiveSignUp()

		if len(self._args) < 3:
			raise core.command.exception(_('ERROR_SIGNUP_NOT_ENOUGH_ARGUMENTS'))

		errors = dict()
		(login, genderId, speciesId) = self._args
		if len(player.model.loadBy({'login': login})):
			raise player.exception(_('ERROR_SIGNUP_LOGIN_ALREADY_USED'))

		genders = [str(g['id_gender']) for g in gender.model.loadAll()]
		if genderId not in genders:
			raise player.exception(_('ERROR_SIGNUP_INVALID_GENDER'))

		sps = [str(s['id_species']) for s in species.model.getSpecies()]
		if speciesId not in sps:
			raise player.exception(_('ERROR_SIGNUP_INVALID_SPECIES'))

		self._player.createNewPlayer(login, speciesId, genderId)
		return login


	def interactiveSignUp(self): # pragma: no cover
		login = None
		while login is None or login == '':
			login = utils.read(_('LOGIN_PROMPT'))

			if len(player.model.loadBy({'login': login})):
				print(_('ERROR_SIGNUP_LOGIN_ALREADY_USED'))
				login = None

		genders = gender.model.loadAll()
		nbGenders = len(genders)

		print(_('GENDER_SELECTION'))
		for k, v in enumerate(genders):
			print(str(k).rjust(3) + ' - ' + v['name'])

		g = -1
		while g < 0 or g >= nbGenders:
			g = utils.read(_('GENDER_PROMPT'))
			try:
				g = int(g)
			except:
				g = -1

		genderId = genders[g]['id_gender']

		sps = species.model.getSpecies()
		nbSpecies = len(sps)

		if nbSpecies == 1:
			speciesId = sps[0]['id_species']
		else:
			print(_('SPECIES_SELECTION'))
			for k, v in enumerate(sps):
				print(str(k).rjust(3) + ' - ' + v['name'])
				print(v['description'])

			sp = -1
			while sp < 0 or sp >= nbSpecies:
				sp = utils.read(_('SPECIES_PROMPT'))
				try:
					sp = int(sp)
				except:
					sp = -1

			speciesId = sps[sp]['id_species']

		self._player.createNewPlayer(login, speciesId, genderId)
		return login

	def render(self, data):
		if len(data) > 0:
			return _('PLAYER_CREATION_CONFIRMATION')
