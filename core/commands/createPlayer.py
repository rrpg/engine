# -*- coding: utf-8 -*-

import core.command
from core.localisation import _
from models import player, gender, species, saved_game

class createPlayer(core.command.command):
	def run(self):
		if len(self._args) < 4:
			raise core.command.exception(_('ERROR_SIGNUP_NOT_ENOUGH_ARGUMENTS'))

		errors = dict()
		(savedGameId, login, genderId, speciesId) = self._args

		if len(player.model.loadBy({'login': login})):
			raise player.exception(_('ERROR_SIGNUP_LOGIN_ALREADY_USED'))

		savedGame = saved_game.saved_game.loadById(savedGameId)
		if savedGame is None:
			raise saved_game.exception(_('ERROR_SIGNUP_INVALID_SAVED_GAME_ID'))

		genders = [str(g['id_gender']) for g in gender.model.loadAll()]
		if str(genderId) not in genders:
			raise player.exception(_('ERROR_SIGNUP_INVALID_GENDER'))

		sps = [str(s['id_species']) for s in species.model.getSpecies()]
		if str(speciesId) not in sps:
			raise player.exception(_('ERROR_SIGNUP_INVALID_SPECIES'))

		playerId = self._player.createNewPlayer(
			login, speciesId, genderId
		)

		p = player.player.loadById(playerId)
		saved_game.saved_game.cleanSavedGame(savedGameId)
		saved_game.saved_game.updateSavedGame(
			savedGameId,
			{
				'id_player': playerId,
				'id_character': p['id_character']
			}
		)
		return login

	def render(self, data):
		if len(data) > 0:
			return _('PLAYER_CREATION_CONFIRMATION')
