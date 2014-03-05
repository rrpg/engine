# -*- coding: utf8 -*-

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
		'look': 'look',
		'talk': 'talk',
		'move': 'move',
		'enter': 'enter',
		'exit': 'exit',
		'take': 'take',
		'drop': 'drop',
		'inventory': 'inventory',
		'inv': 'inventory',
		'help': 'help'
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

		if cmd in ('quit', 'q'):
			return quit
		elif cmd in command.mapping.keys():
			cmd = getattr(current_module, command.mapping[cmd])()
		else:
			raise exception('Unknown command')

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
		print('Available commands:')
		print('talk <Character name> "<Sentence>": Talk to a character')
		print('move <%s>: Go to the indicated direction' % '|'.join(area.directions))
		print('enter <%s>: enter the selected place (if the place is' % '|'.join(place.types) +
			' available in the current cell)')
		print('exit <%s>: exit the selected place (if the current cell is' % '|'.join(place.types) +
			' the place exit)')
		print('look: See what is in the current area' +
			' (characters, items, neighbour areas...)')
		print('inv|inventory: List the items the player has in his inventory')
		print('take [<quantity>] <item name>: Take some items on the the ground')
		print('drop [<quantity>] <item name>: Drop some items from your inventory')
		print('createPlayer: Not Yet Implemented')
		print('help: Display this help')
		print('quit|q: Quit the game')


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
		print("You are in %s.\n" % (regionName))

		# Display surrounding characters
		characters = character.character.searchByIdArea(areaId)
		# the player is in the result list
		if len(characters) > 1:
			print("You see these characters arround:")
			for c in characters:
				if c._model['id_character'] != self._player._model['id_character']:
					print('    ' + c._model['name'])

		# Display accessible areas
		areas = area.model.getSurroundingAreas(areaId)
		directions = area.area.getValidDirections(areas['directions'])
		if len(directions) is not 0:
			print("You can go:")
			for d in directions:
				print('    ' + d)

		# Display accessible places
		places = place.model.getSurroundingPlaces(areaId)
		if len(places) > 0:
			print("You see the following places:")
			for p in places:
				print('    ' + p['name'])

		# Display surrounding objects
		items = item.inventory.fromStr(
			area.model.loadById(areaId, ['items'])['items']
		)
		if len(items) > 0:
			print("You see the following items:")
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
			raise exception("Where shall I go ?")

		direction = self._args[0]
		if direction not in area.area.getDirections():
			raise exception("%s is not a valid direction" % direction)
		curAreaId = self._player.getAreaId()
		curArea = area.model.loadById(curAreaId)

		a = area.area.getNeighbourgFromDirection(curAreaId, direction)

		if area.area.canGoTo(curArea['directions'], direction) is False or a is None:
			raise exception('I cannot go there')
		else:
			self._player.goTo(a._model['id_area'])
			print('lets go %s' % direction)


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
			raise exception("I cannot enter into nothing.")

		areaType = self._args[0]

		p = place.factory.getFromEntranceArea(self._player.getAreaId(), areaType)
		if p is None:
			raise place.exception('There is no such place here.')
			return

		print('The %s\'s door is opening in front of you...' % (areaType,))

		if p['entrance_id'] is None:
			p = place.factory.generate(p, areaType)
		print('You enter.')
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
			raise exception("I cannot exit out of nothing.")

		areaType = self._args[0]

		p = place.factory.getFromExitArea(self._player.getAreaId(), areaType)
		self._player.goTo(p['id_area'])
		print('You are now outside')


class talk(command):
	"""
	Talk command
	"""

	def run(self):
		"""
		Say something to a character in the player's area.
		"""
		if len(self._args) == 0:
			raise exception("Who must I talk to ?")
		elif len(self._args) == 1:
			raise exception("What must I say ?")

		characterName = self._args[0]
		triggerWord = self._args[1]
		c = character.character.searchByNameAndIdArea(
			characterName, self._player.getAreaId()
		)

		if c is None:
			raise character.exception("Unknown Character")

		s = sentence.loadByCharacterIdAndTriggerWord(
			c.getId(), triggerWord
		)

		if len(s) is 0:
			print("What ?")
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
			raise exception("What shall I take ?")

		if len(self._args) == 1:
			quantity = 1
			name = self._args[0]
		else:
			quantity = int(self._args[0])
			name = self._args[1]

		#~ Item the player want to take
		i = item.model.loadBy({'name': name}, ['id_item'])

		if len(i) == 0:
			raise item.exception("I don't see this here.")

		i = str(i[0]['id_item'])
		#~ Available items in the area
		items = area.area.getItems(self._player.getAreaId())

		if i not in items.keys():
			raise item.exception("I don't see this here.")

		if quantity > items[i]['quantity']:
			raise item.exception("There is not enough items of this kind.")

		i = [int(i)] * quantity
		self._player.addItemsToInventory(i)
		area.area.removeItems(self._player.getAreaId(), i)

		print("You took {0} {1}".format(quantity, name))


class drop(command):
	def run(self):
		"""
		c.run()

		Drop an item being in the inventory. The item will be let on the floor
		of the player's current area.
		"""
		# Check an item to drop is provided
		if len(self._args) == 0:
			raise exception("What shall I drop ?")

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
			raise item.exception("You have none of those.")

		i = str(i[0]['id_item'])
		inv = self._player.getInventory()
		if i not in inv.keys():
			raise item.exception("You have none of those.")
		elif quantity > inv[i]['quantity']:
			raise item.exception("You don't have enough {0} to drop.".format(name))

		# Drop it
		self._player.removeItemsFromInventory(i)
		area.area.addItems(self._player.getAreaId(), i)

		print("You dropped {0} {1}".format(quantity, name))


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
