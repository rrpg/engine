# -*- coding: utf8 -*-

import character
import area
from sentence import sentence
import random
import string

quit = -1


class command():
	def setArgs(self, args):
		self._args = args

	def setPlayer(self, player):
		self._player = player

import player


class factory:
	@staticmethod
	def create(p, commandFull):
		cmd = commandFull[0]
		del commandFull[0]

		if cmd in ("talk", "move")\
			and (not p.isConnected() or not p.connect()):
			raise player.exception(
				"A player must be connected to launch the command %s" % cmd
			)

		if cmd == "look":
			command = look()
		elif cmd == "talk":
			command = talk()
		elif cmd == "move":
			command = move()
		elif cmd == "createPlayer":
			if p.isConnected():
				raise player.exception(
					"You cannot create a new player when you're connected"
				)
		elif cmd in ('quit', 'exit', 'q'):
			return quit
		elif cmd == 'help':
			command = help()
		else:
			raise exception('Unknown command')

		command.setArgs(commandFull)
		command.setPlayer(p)
		return command


class help(command):
	def run(self):
		print('Available commands:')
		print('talk <Character name> "<Sentence>": Talk to a character')
		print('move <%s>: Go to the indicated direction' % '|'.join(area.directions))
		print('look: See what is in the current area' +
			' (characters, items, neighbour areas...)')
		print('createPlayer: Not Yet Implemented')
		print('help: Display this help')
		print('quit|exit|q: Quit the game')


class look(command):
	def run(self):
		# Display surrounding characters
		characters = character.character.searchByPlayer(self._player)
		if len(characters) == 0:
			print("You're alone here.")
		else:
			print("Characters arround:")
			for c in character.character.searchByPlayer(self._player):
				print(c._model['name'])

		# Display accessible areas
		areas = area.area.getSurroundingAreas(self._player._model['id_area'])
		print("You can go " +
			', '.join(filter(lambda k: areas[k] == 1, areas)) + '.')

		# Display surrounding objects
		#@TODO


class move(command):
	def run(self):
		if len(self._args) == 0:
			raise exception("Where shall I go ?")

		direction = self._args[0]
		if direction not in area.directions:
			raise exception("%s is not a valid direction" % direction)

		a = area.area.getByIdCharacterAndDirection(
			self._player._model['id_character'], direction
		)

		if a is None:
			raise exception('I cannot go there')
		else:
			self._player.goTo(a._model['id_area'])
			print('lets go %s' % direction)


class talk(command):
	def run(self):
		if len(self._args) == 0:
			raise exception("Who must I talk to ?")
		elif len(self._args) == 1:
			raise exception("What must I say ?")

		characterName = self._args[0]
		triggerWord = self._args[1]
		c = character.character.searchByNameAndPlayer(
			characterName, self._player
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


class exception(BaseException):
	pass
