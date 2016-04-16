# -*- coding: utf-8 -*-

from core import command_factory, fight
from models.player import player
from models.Model import Model
from models.area import area
from models import saved_game
from models.item_container import container
import os
from core.localisation import _
import core.exception


class Rpg:
	_debug = False

	def __init__(self, debug=False):
		"""
		Rpg's construct. Init the following attributes:
		- self._player
		- self._debug
		- self._action
		"""
		self._savedGame = None
		self._player = player()
		self._debug = debug
		self._action = None
		fight.fight.stopFight()
		area.resetChangedAreas()
		container.resetChangedContainers()

	def initWorld(self, world):
		"""
		Method to init the Rpg's world.
		"""
		if os.path.isfile(world) is False:
			raise core.exception.exception(_('ERROR_UNKNOWN_SELECTED_WORLD'))

		Model.setDB(world)

	def initSavedGame(self, savedGameId):
		"""
		Method to init the saved game to play on.
		"""

		savedGame = saved_game.saved_game.loadById(savedGameId)
		if savedGame is None:
			raise saved_game.exception(
				_('ERROR_RRPG_INIT_INVALID_SAVED_GAME_ID')
			)

		self._savedGame = savedGame

	def createPlayer(self, login, genderId, speciesId):
		"""
		Method to create a new player and update the current saved
		game's data.
		"""
		self._player.createNewPlayer(login, speciesId, genderId)

		savedGameId = self._savedGame['id_saved_game']
		saved_game.saved_game.cleanSavedGame(savedGameId)
		saved_game.saved_game.updateSavedGame(
			savedGameId,
			{
				'id_player': self._player._model['id_player'],
				'id_character': self._player._model['id_character'],
				'snapshot_player':  self._player.getSnapshot()
			}
		)
		self._savedGame = saved_game.saved_game.loadById(savedGameId)

	def initPlayer(self):
		"""
		Method to init the player with the current saved game's data.
		"""
		if self._savedGame is None:
			raise core.exception.exception(_('ERROR_SAVED_GAME_NEEDED_TO_INIT_PLAYER'))

		playerData = player.decodeSnapshot(self._savedGame['snapshot_player'])
		if playerData is not None:
			self._player.connect(playerData['login'])
		else:
			raise core.exception.exception(_('ERROR_NON_EMPTY_SAVED_GAME_NEEDED_TO_INIT_PLAYER'))

	def setAction(self, action):
		'''
		Set the action to run
		'''
		if type(action) != list:
			raise TypeError(_('ERROR_INVALID_FORMAT_ACTION'))
		self._action = action

	def isGameOver(self):
		return not self._player.isAlive()

	def _runAction(self, renderJson=False):
		"""
		Method to execute when an action is set and ready to be executed.
		"""
		if self._savedGame is None:
			raise core.exception.exception(_('ERROR_SAVED_GAME_NEEDED_TO_RUN_ACTION'))
		elif not self._player.isConnected():
			raise core.exception.exception(_('ERROR_CONNECTED_PLAYER_NEEDED_FOR_COMMAND'))

		try:
			c = command_factory.factory.create(
				self._player,
				self._action,
				self._savedGame['id_saved_game']
			)

			self._action = None

			if c == command_factory.quit:
				return c

			result = c.run()
			if not renderJson:
				result = c.render(result)
			return result
		except core.exception.exception as e:
			return self.renderException(e, renderJson)

	def renderException(self, e, renderJson=False):
		"""
		Method to call when an exception occurs to render it according to the
		defined render mode.
		"""
		import traceback
		if not isinstance(e, core.exception.exception): # pragma: no cover
			traceback.print_exc()
		else:
			if renderJson:
				excep = {'error': {'code': e.code, 'message': str(e)}}
				if self._debug: # pragma: no cover
					excep['backtrace'] = traceback.format_exc()
				return excep
			elif self._debug: # pragma: no cover
				return traceback.format_exc()
			else:
				return str(e)
