# -*- coding: utf-8 -*-

import core.command
from core.localisation import _
from models import player, gender, species, saved_game

class createPlayer(core.command.command):
	def run(self):
		if len(self._args) < 3:
			raise core.command.exception(_('ERROR_SIGNUP_NOT_ENOUGH_ARGUMENTS'))

		(login, genderId, speciesId) = self._args

		if len(player.model.loadBy({'login': login})):
			raise player.exception(_('ERROR_SIGNUP_LOGIN_ALREADY_USED'))

		genders = [str(g['id_gender']) for g in gender.model.loadAll()]
		if str(genderId) not in genders:
			raise player.exception(_('ERROR_SIGNUP_INVALID_GENDER'))

		sps = [str(s['id_species']) for s in species.model.getSpecies()]
		if str(speciesId) not in sps:
			raise player.exception(_('ERROR_SIGNUP_INVALID_SPECIES'))

		self._player.createNewPlayer(
			login, speciesId, genderId
		)

		saved_game.saved_game.cleanSavedGame(self._savedGameId)
		saved_game.saved_game.updateSavedGame(
			self._savedGameId,
			{
				'id_player': self._player._model['id_player'],
				'id_character': self._player._model['id_character'],
				'snapshot_player':  self._player.getSnapshot()
			}
		)
		return login

	def render(self, data):
		if len(data) > 0:
			return _('PLAYER_CREATION_CONFIRMATION')
