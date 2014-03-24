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

		return [
			{
				'command': '%s <%s> "<%s>"' % (_('TALK_COMMAND'), _('CHARACTER_TOKEN'), _('SENTENCE_TOKEN')),
				'description': _('TALK_COMMAND_DESCRIPTION')
			},
			{
				'command': '%s <%s>' % (_('MOVE_COMMAND'), '|'.join(area.directions)),
				'description': _('MOVE_COMMAND_DESCRIPTION')
			},
			{
				'command': '%s <%s>' % (_('ENTER_COMMAND'), '|'.join(place.types)),
				'description': _('ENTER_COMMAND_DESCRIPTION')
			},
			{
				'command': '%s <%s>' % (_('EXIT_COMMAND'), '|'.join(place.types)),
				'description': _('EXIT_COMMAND_DESCRIPTION')
			},
			{
				'command': _('LOOK_COMMAND'),
				'description': _('LOOK_COMMAND_DESCRIPTION')
			},
			{
				'command': _('INVENTORY_SHORT_COMMAND') + '|' + _('INVENTORY_COMMAND'),
				'description': _('INVENTORY_COMMAND_DESCRIPTION')
			},
			{
				'command': '%s [<%s>] "<%s>"' % (_('TAKE_COMMAND'), _('QUANTITY_TOKEN'), _('ITEM_NAME_TOKEN')),
				'description': _('TAKE_COMMAND_DESCRIPTION')
			},
			{
				'command': '%s [<%s>] "<%s>"' % (_('DROP_COMMAND'), _('QUANTITY_TOKEN'), _('ITEM_NAME_TOKEN')),
				'description': _('DROP_COMMAND_DESCRIPTION')
			},
			{
				'command': _('HELP_COMMAND'),
				'description': _('HELP_COMMAND_DESCRIPTION')
			},
			{
				'command': _('QUIT_SHORT_COMMAND') + '|' + _('QUIT_COMMAND'),
				'description': _('QUIT_COMMAND_DESCRIPTION')
			}
		]

	def render(self, data):
		print(_('AVAILABLE_COMMANDS_TITLE'))
		for c in data:
			print(c['command'] + ':')
			print('\t' + c['description'])
