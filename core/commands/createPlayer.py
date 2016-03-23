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
		if str(genderId) not in genders:
			raise player.exception(_('ERROR_SIGNUP_INVALID_GENDER'))

		sps = [str(s['id_species']) for s in species.model.getSpecies()]
		if str(speciesId) not in sps:
			raise player.exception(_('ERROR_SIGNUP_INVALID_SPECIES'))

		self._player.createNewPlayer(login, speciesId, genderId)
		return login

	def render(self, data):
		if len(data) > 0:
			return _('PLAYER_CREATION_CONFIRMATION')
