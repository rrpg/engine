# -*- coding: utf-8 -*-
import unittest

import tests.common
from core.localisation import _
import core.command_factory
from models import area, place
import json


class helpTests(tests.common.common):
	def test_text(self):
		self.rpg.setAction([_('HELP_COMMAND')])
		output = self.rpg._runAction()
		expected = _('AVAILABLE_COMMANDS_TITLE') +'\n'+\
			'%s <%s> "<%s>"' % (_('TALK_COMMAND'), _('CHARACTER_TOKEN'), _('SENTENCE_TOKEN')) + ':' +'\n'+\
			'\t' + _('TALK_COMMAND_DESCRIPTION') +'\n'+\
			'%s <%s>' % (_('MOVE_COMMAND'), '|'.join([str(s) for s in area.directions])) + ':' +'\n'+\
			'\t' + _('MOVE_COMMAND_DESCRIPTION') +'\n'+\
			'%s <%s>' % (_('ENTER_COMMAND'), '|'.join([str(s) for s in place.types])) + ':' +'\n'+\
			'\t' + _('ENTER_COMMAND_DESCRIPTION') +'\n'+\
			'%s <%s>' % (_('EXIT_COMMAND'), '|'.join([str(s) for s in place.types])) + ':' +'\n'+\
			'\t' + _('EXIT_COMMAND_DESCRIPTION') +'\n'+\
			_('LOOK_COMMAND') + ':' +'\n'+\
			'\t' + _('LOOK_COMMAND_DESCRIPTION') +'\n'+\
			_('INVENTORY_SHORT_COMMAND') + '|' + _('INVENTORY_COMMAND') + ':' +'\n'+\
			'\t' + _('INVENTORY_COMMAND_DESCRIPTION') +'\n'+\
			'%s "<%s>" [<%s>]' % (_('OPEN_COMMAND'), _('CONTAINER_TOKEN'), _('CONTAINER_INDEX_TOKEN')) + ':' +'\n'+\
			'\t' + _('OPEN_COMMAND_DESCRIPTION') +'\n'+\
			'%s [<%s>] "<%s>" ["<%s>" [<%s>]]' % (
				_('TAKE_COMMAND'),
				_('QUANTITY_TOKEN'),
				_('ITEM_NAME_TOKEN'),
				_('CONTAINER_TOKEN'),
				_('CONTAINER_INDEX_TOKEN')
			) + ':' +'\n'+\
			'\t' + _('TAKE_COMMAND_DESCRIPTION') +'\n'+\
			'%s [<%s>] "<%s>" ["<%s>" [<%s>]]' % (
				_('DROP_COMMAND'),
				_('QUANTITY_TOKEN'),
				_('ITEM_NAME_TOKEN'),
				_('CONTAINER_TOKEN'),
				_('CONTAINER_INDEX_TOKEN')
			) + ':' +'\n'+\
			'\t' + _('DROP_COMMAND_DESCRIPTION') +'\n'+\
			_('STATS_COMMAND') + ':' +'\n'+\
			'\t' + _('STATS_COMMAND_DESCRIPTION') +'\n'+\
			_('ATTACK_COMMAND') + ':' +'\n'+\
			'\t' + _('ATTACK_COMMAND_DESCRIPTION') +'\n'+\
			_('SAVE_COMMAND') + ':' +'\n'+\
			'\t' + _('SAVE_COMMAND_DESCRIPTION') +'\n'+\
			_('HELP_COMMAND') + ':' +'\n'+\
			'\t' + _('HELP_COMMAND_DESCRIPTION') +'\n'+\
			_('QUIT_SHORT_COMMAND') + '|' + _('QUIT_COMMAND') + ':' +'\n'+\
			'\t' + _('QUIT_COMMAND_DESCRIPTION')
		self.assertEquals(output, expected)

	def test_json(self):
		self.rpg.setAction([_('HELP_COMMAND')])
		output = self.rpg._runAction(True)
		expected = [
			{
				"command": '%s <%s> "<%s>"' % (_('TALK_COMMAND'), _('CHARACTER_TOKEN'), _('SENTENCE_TOKEN')),
				"description": _('TALK_COMMAND_DESCRIPTION')
			},
			{
				"command": '%s <%s>' % (_('MOVE_COMMAND'), '|'.join([str(s) for s in area.directions])),
				"description": _('MOVE_COMMAND_DESCRIPTION')
			},
			{
				"command": '%s <%s>' % (_('ENTER_COMMAND'), '|'.join([str(s) for s in place.types])),
				"description": _('ENTER_COMMAND_DESCRIPTION')
			},
			{
				"command": '%s <%s>' % (_('EXIT_COMMAND'), '|'.join([str(s) for s in place.types])),
				"description": _('EXIT_COMMAND_DESCRIPTION')
			},
			{
				"command": _('LOOK_COMMAND'),
				"description": _('LOOK_COMMAND_DESCRIPTION')
			},
			{
				"command": _('INVENTORY_SHORT_COMMAND') + '|' + _('INVENTORY_COMMAND'),
				"description": _('INVENTORY_COMMAND_DESCRIPTION')
			},
			{
				"command": '%s "<%s>" [<%s>]' % (_('OPEN_COMMAND'), _('CONTAINER_TOKEN'), _('CONTAINER_INDEX_TOKEN')),
				"description": _('OPEN_COMMAND_DESCRIPTION')
			},
			{
				"command": '%s [<%s>] "<%s>" ["<%s>" [<%s>]]' % (_('TAKE_COMMAND'), _('QUANTITY_TOKEN'), _('ITEM_NAME_TOKEN'), _('CONTAINER_TOKEN'), _('CONTAINER_INDEX_TOKEN')),
				"description": _('TAKE_COMMAND_DESCRIPTION')
			},
			{
				"command": '%s [<%s>] "<%s>" ["<%s>" [<%s>]]' % (_('DROP_COMMAND'), _('QUANTITY_TOKEN'), _('ITEM_NAME_TOKEN'), _('CONTAINER_TOKEN'), _('CONTAINER_INDEX_TOKEN')),
				"description": _('DROP_COMMAND_DESCRIPTION')
			},
			{
				"command": _('STATS_COMMAND'),
				"description": _('STATS_COMMAND_DESCRIPTION')
			},
			{
				"command": _('ATTACK_COMMAND'),
				"description": _('ATTACK_COMMAND_DESCRIPTION')
			},
			{
				"command": _('SAVE_COMMAND'),
				"description": _('SAVE_COMMAND_DESCRIPTION')
			},
			{
				"command": _('HELP_COMMAND'),
				"description": _('HELP_COMMAND_DESCRIPTION')
			},
			{
				"command": _('QUIT_SHORT_COMMAND') + '|' + _('QUIT_COMMAND'),
				"description": _('QUIT_COMMAND_DESCRIPTION')
			}
		]

		self.assertEquals(output, expected)
		self.assertEquals(len(output), len(core.command_factory.factory.mapping))
