# -*- coding: utf-8 -*-

"""
Module containing the available commands of the game, the factory class to
create the commands...
Today, the available commands are:
- help
- look
- move
- quit|q|exit
- talk
"""

import sys
import character
import area
import random
import string
import player
import item
import place
from sentence import sentence
from localisation import _

"""
Code corresponding to the quit command
"""
quit = -1

# Store current module for the factory
current_module = sys.modules[__name__]


class command():
	"""
	Base class for the commands
	"""

	"""
	Available commands stored in a dict with as key, the commands and as value,
	the command class to execute.
	"""
	mapping = {
		_('LOOK_COMMAND'): 'look',
		_('TALK_COMMAND'): 'talk',
		_('MOVE_COMMAND'): 'move',
		_('ENTER_COMMAND'): 'enter',
		_('EXIT_COMMAND'): 'exit',
		_('TAKE_COMMAND'): 'take',
		_('DROP_COMMAND'): 'drop',
		_('INVENTORY_COMMAND'): 'inventory',
		_('INVENTORY_SHORT_COMMAND'): 'inventory',
		_('HELP_COMMAND'): 'help'
	}

	def setArgs(self, args):
		"""
		c.setArgs(args)

		Define the arguments of the command.

		@params list arguments of the command to run
		"""
		self._args = args

	def setPlayer(self, p):
		"""
		c.setPlayer(p)

		Define the current player in the command's context.

		@params player.player
		"""
		self._player = p


class factory:
	"""
	Class to instanciate a command from a string.
	"""

	@staticmethod
	def create(p, commandFull):
		"""
		command.factory.create(p, commandFull) -> command.command

		Create the desired command.

		@param p player.player Current player.
		@param commandFull list command to run, the first element of the list
			is the command, the other elements are the command's arguments.

		@return the created command
		"""

		cmd = commandFull[0]
		del commandFull[0]

		if cmd not in ("createPlayer", "help")\
			and (not p.isConnected() or not p.connect()):
			raise player.exception(
				"A player must be connected to launch the command %s" % cmd
			)

		if cmd in (_('QUIT_COMMAND'), _('QUIT_SHORT_COMMAND')):
			return quit
		elif cmd in command.mapping.keys():
			cmd = getattr(current_module, command.mapping[cmd])()
		else:
			raise exception(_('ERROR_UNKNOWN_COMMAND'))

		cmd.setArgs(commandFull)
		cmd.setPlayer(p)
		return cmd


class completer:
	"""
	Class to autocomplete use choice while typing a command
	"""

	def __init__(self):
		"""
		Construct. Set the available commands in an options var
		"""
		self.options = sorted(command.mapping.keys())

	def complete(self, text, state):
		"""
		Called method when autocomplete is invoqued
		"""

		# on first trigger, build possible matches
		if state == 0:
			# cache matches (entries that start with entered text)
			if len(text.split(' ')) > 1:
				return text

			if text:
				self.matches = [s for s in self.options if s and s.startswith(text)]
			# no text entered, all matches possible
			else:
				self.matches = self.options[:]

		# return match indexed by state
		try:
			return self.matches[state]
		except IndexError as e:
			return None


class help(command):
	"""
	Help command
	"""

	def run(self):
		"""
		c.run()

		Display a help message.
		"""
		print(_('AVAILABLE_COMMANDS_TITLE'))
		print('%s <%s> "<%s>":' % (_('TALK_COMMAND'), _('CHARACTER_TOKEN'), _('SENTENCE_TOKEN')))
		print('\t' + _('TALK_COMMAND_DESCRIPTION'))
		print('%s <%s>:' % (_('MOVE_COMMAND'), '|'.join(area.directions)))
		print('\t' + _('MOVE_COMMAND_DESCRIPTION'))
		print('%s <%s>:' % (_('ENTER_COMMAND'), '|'.join(place.types)))
		print('\t' + _('ENTER_COMMAND_DESCRIPTION'))
		print('%s <%s>:' % (_('EXIT_COMMAND'), '|'.join(place.types)))
		print('\t' + _('EXIT_COMMAND_DESCRIPTION'))
		print(_('LOOK_COMMAND') + ':')
		print('\t' + _('LOOK_COMMAND_DESCRIPTION'))
		print(_('INVENTORY_SHORT_COMMAND') + '|' + _('INVENTORY_COMMAND') + ':')
		print('\t' + _('INVENTORY_COMMAND_DESCRIPTION'))
		print('%s [<%s>] "<%s>":' % (_('TAKE_COMMAND'), _('QUANTITY_TOKEN'), _('ITEM_NAME_TOKEN')))
		print('\t' + _('TAKE_COMMAND_DESCRIPTION'))
		print('%s [<%s>] "<%s>":' % (_('DROP_COMMAND'), _('QUANTITY_TOKEN'), _('ITEM_NAME_TOKEN')))
		print('\t' + _('DROP_COMMAND_DESCRIPTION'))
		# print('createPlayer:')
		# print('\t' + 'Not Yet Implemented')
		print(_('HELP_COMMAND') + ':')
		print('\t' + _('HELP_COMMAND_DESCRIPTION'))
		print(_('QUIT_SHORT_COMMAND') + '|' + _('QUIT_COMMAND') + ':')
		print('\t' + _('QUIT_COMMAND_DESCRIPTION'))


class look(command):
	"""
	Look command
	"""
	def run(self):
		"""
		c.run()

		Display some informations about the player's current position
		(characters arround, availables directions...).
		"""
		areaId = self._player.getAreaId()

		# Display current area description
		regionName = area.area.getRegionNameFromAreaId(areaId)
		print(_('CURRENT_REGION_%s') % (regionName))
		print('\n')

		# Display surrounding characters
		characters = character.character.searchByIdArea(areaId)
		# the player is in the result list
		if len(characters) > 1:
			print(_('PRESENT_CHARACTERS'))
			for c in characters:
				if c._model['id_character'] != self._player._model['id_character']:
					print('    ' + c._model['name'])

		# Display accessible areas
		areas = area.model.getSurroundingAreas(areaId)
		directions = area.area.getValidDirections(areas['directions'])
		if len(directions) is not 0:
			print(_('AVAILABLE_DIRECTIONS'))
			for d in directions:
				print('    ' + d)

		# Display accessible places
		places = place.model.getSurroundingPlaces(areaId)
		if len(places) > 0:
			print(_('AVAILABLE_PLACES'))
			for p in places:
				print('    ' + p['name'])

		# Display surrounding objects
		items = item.inventory.fromStr(
			area.model.loadById(areaId, ['items'])['items']
		)
		if len(items) > 0:
			print(_('AVAILABLE_ITEMS'))
			for i in items:
				it = item.model.loadById(i)
				print(str(items[i]['quantity']).rjust(3) + ' ' + it['name'])


class move(command):
	"""
	Move command
	"""

	def run(self):
		"""
		c.run()

		Move the player in the desired direction.
		"""
		if len(self._args) == 0:
			raise exception(_('ERROR_MOVE_NO_DIRECTION_GIVEN'))

		direction = self._args[0]
		if direction not in area.area.getDirections():
			raise exception(_('ERROR_MOVE_INVALID_DIRECTION_%s') % direction)
		curAreaId = self._player.getAreaId()
		curArea = area.model.loadById(curAreaId)

		a = area.area.getNeighbourgFromDirection(curAreaId, direction)

		if area.area.canGoTo(curArea['directions'], direction) is False or a is None:
			raise exception(_('ERROR_MOVE_DIRECTION_NOT_AVAILABLE'))
		else:
			self._player.goTo(a._model['id_area'])
			print(_('MOVE_CONFIRMATION_%s') % direction)


class enter(command):
	"""
	Enter command
	"""

	def run(self):
		"""
		c.run()

		With this command, the player can enter places such as houses, shops,
		dungeons...
		"""
		if len(self._args) == 0:
			raise exception(_('ERROR_ENTER_NO_PLACE_GIVEN'))

		areaType = self._args[0]

		p = place.factory.getFromEntranceArea(self._player.getAreaId(), areaType)
		if p is None:
			raise place.exception(_('ERROR_ENTER_PLACE_NOT_AVAILABLE'))
			return

		if p['entrance_id'] is None:
			p = place.factory.generate(p, areaType)
		print(_('ENTER_CONFIRMATION'))
		self._player.goTo(p['entrance_id'])


class exit(command):
	"""
	Exit command, to exit a place
	"""

	def run(self):
		"""
		c.run()

		With this command, the player can exit places such as houses, shops,
		dungeons... to go back in the world
		"""
		if len(self._args) == 0:
			raise exception(_('ERROR_EXIT_NO_PLACE_GIVEN'))

		areaType = self._args[0]

		p = place.factory.getFromExitArea(self._player.getAreaId(), areaType)
		if p is None:
			raise place.exception(_('ERROR_ENTER_PLACE_NOT_AVAILABLE'))
			return

		self._player.goTo(p['id_area'])
		print(_('EXIT_CONFIRMATION'))


class talk(command):
	"""
	Talk command
	"""

	def run(self):
		"""
		Say something to a character in the player's area.
		"""
		if len(self._args) == 0:
			raise exception(_('ERROR_TALK_NO_CHARACTER_GIVEN'))
		elif len(self._args) == 1:
			raise exception(_('ERROR_TALK_NO_SENTENCE_GIVEN'))

		characterName = self._args[0]
		triggerWord = self._args[1]
		c = character.character.searchByNameAndIdArea(
			characterName, self._player.getAreaId()
		)

		if c is None:
			raise character.exception(_('ERROR_TALK_UNKNOWN_CHARACTER'))

		s = sentence.loadByCharacterIdAndTriggerWord(
			c.getId(), triggerWord
		)

		if len(s) is 0:
			print(_('ERROR_TALK_UNKNOWN_SENTENCE'))
			return

		s = s[random.randint(0, len(s) - 1)]
		print(self.processSentence(
			s.getSentence(), self._player._model['name']
		))

	def processSentence(self, s, characterName):
		return s % {'player_name': characterName}


class take(command):
	def run(self):
		if len(self._args) == 0:
			raise exception(_('ERROR_TAKE_NO_ITEM_GIVEN'))

		if len(self._args) == 1:
			quantity = 1
			name = self._args[0]
		else:
			quantity = int(self._args[0])
			name = self._args[1]

		#~ Item the player want to take
		i = item.model.loadBy({'name': name}, ['id_item'])

		if len(i) == 0:
			raise item.exception(_('ERROR_TAKE_UNKNOWN_ITEM'))

		i = str(i[0]['id_item'])
		#~ Available items in the area
		items = area.area.getItems(self._player.getAreaId())

		if i not in items.keys():
			raise item.exception(_('ERROR_TAKE_ITEM_NOT_AVAILABLE'))

		if quantity > items[i]['quantity']:
			raise item.exception(_('ERROR_TAKE_QUANTITY_TOO_HIGH'))

		i = [int(i)] * quantity
		self._player.addItemsToInventory(i)
		area.area.removeItems(self._player.getAreaId(), i)

		print(_('TAKE_CONFIRMATION_%(quantity)s_%(name)s') % {'quantity': quantity, 'name': name})


class drop(command):
	def run(self):
		"""
		c.run()

		Drop an item being in the inventory. The item will be let on the floor
		of the player's current area.
		"""
		# Check an item to drop is provided
		if len(self._args) == 0:
			raise exception(_('ERROR_DROP_NO_ITEM_GIVEN'))

		# check if a quantity is provided
		if len(self._args) == 1:
			quantity = 1
			name = self._args[0]
		else:
			quantity = int(self._args[0])
			name = self._args[1]

		# Item the player want to drop
		i = item.model.loadBy({'name': name}, ['id_item'])

		if len(i) == 0:
			raise item.exception(_('ERROR_DROP_UNKNOWN_ITEM'))

		i = str(i[0]['id_item'])
		inv = self._player.getInventory()
		if i not in inv.keys():
			raise item.exception(_('ERROR_DROP_ITEM_NOT_AVAILABLE'))
		elif quantity > inv[i]['quantity']:
			raise item.exception(_('ERROR_DROP_QUANTITY_TOO_HIGH_%s') % name)

		# Drop it
		self._player.removeItemsFromInventory(i)
		area.area.addItems(self._player.getAreaId(), i)

		print(_('DROP_CONFIRMATION_%(quantity)s_%(name)s') % {'quantity': quantity, 'name': name})


class inventory(command):
	def run(self):
		"""
		c.run()

		Display the player's inventory.
		"""

		i = self._player.getInventory()
		for itemId in i:
			it = item.model.loadById(itemId)
			print(str(i[itemId]['quantity']).rjust(3) + ' ' + it['name'])


class exception(BaseException):
	"""
	Class for the exceptions concerning commands.
	"""
	pass
