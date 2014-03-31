# -*- coding: utf-8 -*-
import unittest
import sys
import os
sys.path.append(os.path.realpath(__file__ + "/../../../"))

import tests.common
from tests.output_capturer import capturer
from core.localisation import _
from models import area, place
import json


class helpTests(tests.common.common):
	def test_text(self):
		self.rpgText.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', [_('HELP_COMMAND')])
		with capturer() as output:
			self.rpgText._runAction()
		expected = [
			_('AVAILABLE_COMMANDS_TITLE'),
			'%s <%s> "<%s>"' % (_('TALK_COMMAND'), _('CHARACTER_TOKEN'), _('SENTENCE_TOKEN')) + ':',
			'\t' + _('TALK_COMMAND_DESCRIPTION'),
			'%s <%s>' % (_('MOVE_COMMAND'), '|'.join([str(s) for s in area.directions])) + ':',
			'\t' + _('MOVE_COMMAND_DESCRIPTION'),
			'%s <%s>' % (_('ENTER_COMMAND'), '|'.join([str(s) for s in place.types])) + ':',
			'\t' + _('ENTER_COMMAND_DESCRIPTION'),
			'%s <%s>' % (_('EXIT_COMMAND'), '|'.join([str(s) for s in place.types])) + ':',
			'\t' + _('EXIT_COMMAND_DESCRIPTION'),
			_('LOOK_COMMAND') + ':',
			'\t' + _('LOOK_COMMAND_DESCRIPTION'),
			_('INVENTORY_SHORT_COMMAND') + '|' + _('INVENTORY_COMMAND') + ':',
			'\t' + _('INVENTORY_COMMAND_DESCRIPTION'),
			'%s [<%s>] "<%s>"' % (_('TAKE_COMMAND'), _('QUANTITY_TOKEN'), _('ITEM_NAME_TOKEN')) + ':',
			'\t' + _('TAKE_COMMAND_DESCRIPTION'),
			'%s [<%s>] "<%s>"' % (_('DROP_COMMAND'), _('QUANTITY_TOKEN'), _('ITEM_NAME_TOKEN')) + ':',
			'\t' + _('DROP_COMMAND_DESCRIPTION'),
			_('HELP_COMMAND') + ':',
			'\t' + _('HELP_COMMAND_DESCRIPTION'),
			_('QUIT_SHORT_COMMAND') + '|' + _('QUIT_COMMAND') + ':',
			'\t' + _('QUIT_COMMAND_DESCRIPTION')
		]
		self.assertTrue(output == expected)

	def test_json(self):
		self.rpgJSON.init(self.dbFile, 'TEST_PLAYER', 'TEST_PLAYER', [_('HELP_COMMAND')])
		with capturer() as output:
			self.rpgJSON._runAction()
		expected = '[{"command": "' \
			+ ('%s <%s> \\"<%s>\\"' % (_('TALK_COMMAND'), _('CHARACTER_TOKEN'), _('SENTENCE_TOKEN'))) \
			+ '", "description": "' + _('TALK_COMMAND_DESCRIPTION') \
			+ '"}, {"command": "' \
			+ ('%s <%s>' % (_('MOVE_COMMAND'), '|'.join([str(s) for s in area.directions]))) \
			+ '", "description": "' + _('MOVE_COMMAND_DESCRIPTION') \
			+ '"}, {"command": "'\
			+ ('%s <%s>' % (_('ENTER_COMMAND'), '|'.join([str(s) for s in place.types])))\
			+ '", "description": "' + _('ENTER_COMMAND_DESCRIPTION')\
			+ '"}, {"command": "'\
			+ ('%s <%s>' % (_('EXIT_COMMAND'), '|'.join([str(s) for s in place.types])))\
			+ '", "description": "' + _('EXIT_COMMAND_DESCRIPTION')\
			+ '"}, {"command": "' + _('LOOK_COMMAND')\
			+ '", "description": "' + _('LOOK_COMMAND_DESCRIPTION')\
			+ '"}, {"command": "'\
			+ _('INVENTORY_SHORT_COMMAND') + '|' + _('INVENTORY_COMMAND')\
			+ '", "description": "' + _('INVENTORY_COMMAND_DESCRIPTION')\
			+ '"}, {"command": "'\
			+ ('%s [<%s>] \\"<%s>\\"' % (_('TAKE_COMMAND'), _('QUANTITY_TOKEN'), _('ITEM_NAME_TOKEN')))\
			+ '", "description": "' + _('TAKE_COMMAND_DESCRIPTION')\
			+ '"}, {"command": "'\
			+ ('%s [<%s>] \\"<%s>\\"' % (_('DROP_COMMAND'), _('QUANTITY_TOKEN'), _('ITEM_NAME_TOKEN')))\
			+ '", "description": "' + _('DROP_COMMAND_DESCRIPTION')\
			+ '"}, {"command": "' + _('HELP_COMMAND')\
			+ '", "description": "' + _('HELP_COMMAND_DESCRIPTION')\
			+ '"}, {"command": "'\
			+ _('QUIT_SHORT_COMMAND') + '|' + _('QUIT_COMMAND')\
			+ '", "description": "' + _('QUIT_COMMAND_DESCRIPTION') + '"}]'

		output = json.loads(output[0])
		expected = json.loads(expected)

		self.assertTrue(output == expected)
unittest.main()
