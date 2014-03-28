import unittest
import sys
import os
sys.path.append(os.path.realpath(__file__ + "/../../../"))

import tests.common
from tests.output_capturer import capturer


class helpTests(tests.common.common):
	def test_text(self):
		self.rpgText.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', ['help'])
		with capturer() as output:
			self.rpgText._runAction()
		self.assertTrue(output == [
			'Available commands',
			'talk <character name> "<sentence>":',
			'\tTalk to a character',
			'move <west|east|north|south>:',
			'\tGo to the indicated direction',
			'enter <dungeon|cave>:',
			'\tEnter in the selected place (if the place is available in the current cell)',
			'exit <dungeon|cave>:',
			'\tExit from the selected place (if the current cell is the place exit)',
			'look:',
			'\tList everything which is in the current area (characters, items, neighbour areas...)',
			'inv|inventory:',
			'\tList the items the player has in his inventory',
			'take [<quantity>] "<item name>":',
			'\tTake some items on the ground',
			'drop [<quantity>] "<item name>":',
			'\tDrop some items from your inventory',
			'help:',
			'\tDisplay the help menu',
			'q|quit:',
			'\tQuit the game'
		])

	def test_json(self):
		self.rpgJSON.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', ['help'])
		with capturer() as output:
			self.rpgJSON._runAction()
		self.assertTrue(output == ['[{"command": "talk <character name> \\"<sentence>\\"", "description": "Talk to a character"}, {"command": "move <west|east|north|south>", "description": "Go to the indicated direction"}, {"command": "enter <dungeon|cave>", "description": "Enter in the selected place (if the place is available in the current cell)"}, {"command": "exit <dungeon|cave>", "description": "Exit from the selected place (if the current cell is the place exit)"}, {"command": "look", "description": "List everything which is in the current area (characters, items, neighbour areas...)"}, {"command": "inv|inventory", "description": "List the items the player has in his inventory"}, {"command": "take [<quantity>] \\"<item name>\\"", "description": "Take some items on the ground"}, {"command": "drop [<quantity>] \\"<item name>\\"", "description": "Drop some items from your inventory"}, {"command": "help", "description": "Display the help menu"}, {"command": "q|quit", "description": "Quit the game"}]'])

unittest.main()
