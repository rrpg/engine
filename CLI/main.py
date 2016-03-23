# -*- coding: utf-8 -*-

import core
import core.Rpg
from core import utils
from models import player, gender, species
from core.localisation import _
from core import command, command_factory
import readline


class main:
	_debug = False

	def __init__(self, debug=False, world='', login=None):
		self._engine = core.Rpg.Rpg(debug)

		try:
			self._engine.init(world, login)
			if login is None:
				login = self._doInteractiveAuth()
		except (KeyboardInterrupt, EOFError):
			print("")
			return
		except BaseException as e:
			e = self._engine.renderException(e)
			if e is not None:
				print(e)
			return

		self.run()

	def _doInteractiveAuth(self): # pragma: no cover
		'''
		This method asks the player to login or to create a new account
		'''
		choice = 0
		print(_('PLAYER_SELECTION'))
		print("  1 - " + _('CHOICE_NEW_PLAYER'))
		print("  2 - " + _('CHOICE_EXISTING_PLAYER'))
		while choice != 1 and choice != 2:
			try:
				choice = int(utils.read(_('CHOICE_QUESTION')))
			except ValueError:
				# If the typed value is not a valid integer
				pass

		if choice == 1:
			(login, genderId, speciesId) = self._interactivePlayerCreation()
			self._engine.setAction(['create-player', login, genderId, speciesId])
			print(self._engine._runAction())
		elif choice == 2:
			login = self._promptLoginFromStdin()

		self._engine._initPlayer(login)
		return login

	def _interactivePlayerCreation(self): # pragma: no cover
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

		return (login, genderId, speciesId)

	def _promptLoginFromStdin(self): # pragma: no cover
		'''
		Ask the player to type his login
		'''
		login = ''
		while login == '':
			login = utils.read(_('LOGIN_PROMPT'))

		return login

	def _gameOver(self): # pragma: no cover
		print(_('GAME_OVER_TEXT'))

	def run(self): # pragma: no cover
		'''
		Main method of the Rpg Class, will ask the player to enter a command
		'''
		c = ''
		result = 0
		while not self._engine.isGameOver():
			try:
				c = self.readCommand()
			except KeyboardInterrupt:
				print("")
				continue
			except EOFError:
				print("")
				break

			if c != "":
				self._engine.setAction(self.parseTypedAction(c))
				result = self._engine._runAction()

			if result == command_factory.quit:
				break
			elif c != "":
				print(result)
				print("")

		self._gameOver()

	def parseTypedAction(self, action):
		"""
		Method to parse the action typed by the player to detect the action
		and the action's arguments
		"""
		inOption = False

		commands, sep, option, optionStart = list(), ' ', '', 0
		commandLen = len(action)
		for k,i in enumerate(action):
			# first letter of the option
			if i != ' ' and not inOption:
				# Set the start index of the option
				optionStart = k
				inOption = True
				# Set the option delimiter
				sep = i if i in ("'", '"') else ' '
			if inOption:
				# If the current char is the option delimiter, but not the
				# stat one
				if i == sep and k > optionStart:
					# The option is ended
					inOption = False
				elif i != sep:
					option += i

				# The option is complete, append it in the list
				if not inOption or k == commandLen - 1:
					commands.append(str(option))
					option = ''

		return commands

	def readCommand(self): # pragma: no cover
		"""
		Method to set the autocompleter and run the prompt, from utils
		"""

		completer = command.completer(
			sorted(command_factory.factory.mapping.keys())
		)
		readline.set_completer(completer.complete)
		readline.parse_and_bind('tab: complete')
		readline.set_completer_delims('')
		return utils.read(_('COMMAND_PROMPT'))
