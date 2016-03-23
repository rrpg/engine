# -*- coding: utf-8 -*-

from models.player import player
from core import command, command_factory, utils, config, fight
from models.Model import Model
from models.area import area
from models.item_container import container
import readline
import getpass
import os
import json
from core.localisation import _
import core.exception

RENDER_TEXT = 0
RENDER_JSON = 1

class Rpg:
	_debug = False

	def __init__(self, debug=False, renderMode=RENDER_TEXT, isInteractive=True):
		"""
		Rpg's construct. Init the following attributes:
		- self._player
		- self._debug
		- self._renderMode
		- self._action
		- self._isInteractive

		The render mode can be or RENDER_TEXT or RENDER_JSON.
		If the flag isInteractive is set to False, the game will just execute
		the next action without entering the game loop, no command will be
		prompted to the user. This can be used for the tests or when the game is
		used as a service.
		"""
		self._player = None
		self._debug = debug
		self._renderMode = renderMode
		self._action = []
		self._isInteractive = isInteractive
		fight.fight.stopFight()
		area.resetChangedAreas()
		container.resetChangedContainers()

	def init(self, world, login=None):
		"""
		Method to init the Rpg with a world, a player's login and action. The
		action is optional, but the login can be None (for
		unauthentified actions such as createPlayer for example).

		Will raise an core.exception.exception if no login is provided
		and the provided action needs player.
		"""
		if os.path.isfile(world) is False:
			raise core.exception.exception(_('ERROR_UNKNOWN_SELECTED_WORLD'))

		Model.setDB(world)
		self._initPlayer(login)

	def _initPlayer(self, login):
		"""
		Method to init the player with a login.
		"""
		self._player = player()

		if login is not None:
			self._player.connect(login)

	def setAction(self, action):
		'''
		Set the action to run
		'''
		if type(action) != list:
			raise TypeError(_('ERROR_INVALID_FORMAT_ACTION'))
		self._action = action


	def _runAction(self):
		"""
		Method to execute when an action is set and ready to be executed.
		"""
		try:
			c = command_factory.factory.create(
				self._player,
				self._action,
				self._isInteractive
			)

			if c == command_factory.quit:
				return c

			result = c.run()
			if self._renderMode != RENDER_JSON:
				result = c.render(result)
			return result
		except core.exception.exception as e:
			return self.renderException(e)

	def renderException(self, e): # pragma: no cover
		"""
		Method to call when an exception occurs to render it according to the
		defined render mode.
		"""
		import traceback
		if not isinstance(e, core.exception.exception):
			traceback.print_exc()
		else:
			if self._renderMode == RENDER_JSON:
				excep = {'error': {'code': e.code, 'message': str(e)}}
				if self._debug:
					excep['backtrace'] = traceback.format_exc()
				return excep
			elif self._debug:
				return traceback.format_exc()
			else:
				return str(e)
