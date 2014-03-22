# -*- coding: utf-8 -*-

from models import area, place
import core.command
from core.localisation import _


class help(core.command.command):
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

	def render(self, data):
		pass
