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

	mapping = {
		'look': 'look',
		'talk': 'talk',
		'move': 'move',
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

		if cmd in ('quit', 'exit', 'q'):
			return quit
		elif cmd in command.mapping.keys():
			cmd = getattr(current_module, command.mapping[cmd])()
		else:
			raise exception('Unknown command')

		cmd.setArgs(commandFull)
		cmd.setPlayer(p)
		return cmd


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
		print('look: See what is in the current area' +
			' (characters, items, neighbour areas...)')
		print('inv|inventory: List the items the player has in his inventory')
		print('take [<quantity>] <item name>: Take some items on the the ground')
		print('drop [<quantity>] <item name>: Drop some items from your inventory')
		print('createPlayer: Not Yet Implemented')
		print('help: Display this help')
		print('quit|exit|q: Quit the game')


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
		# Display surrounding characters
		characters = character.character.searchByIdArea(self._player._model['id_area'])
		# the player is in the result list
		if len(characters) == 1:
			print("You're alone here.")
		else:
			print("Characters arround:")
			for c in characters:
				if c._model['id_character'] != self._player._model['id_character']:
					print(c._model['name'])

		# Display accessible areas
		areas = area.model.getSurroundingAreas(self._player._model['id_area'])
		print("You can go " +
			', '.join(filter(lambda k: areas[k] == 1, areas)) + '.')

		# Display surrounding objects
		items = item.inventory.fromStr(
			area.model.loadById(self._player._model['id_area'], ['items'])['items']
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
		if direction not in area.directions:
			raise exception("%s is not a valid direction" % direction)

		a = area.area.getNeighbourgFromDirection(
			self._player._model['id_area'], direction
		)

		if a is None:
			raise exception('I cannot go there')
		else:
			self._player.goTo(a._model['id_area'])
			print('lets go %s' % direction)


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
			characterName, self._player._model['id_area']
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
		items = area.area.getItems(self._player._model['id_area'])

		if i not in items.keys():
			raise item.exception("I don't see this here.")

		if quantity > items[i]['quantity']:
			raise item.exception("There is not enough items of this kind.")

		i = [int(i)] * quantity
		self._player.addItemsToInventory(i)
		area.area.removeItems(self._player._model['id_area'], i)

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
		area.area.addItems(self._player._model['id_area'], i)

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
