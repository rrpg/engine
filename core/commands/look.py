# -*- coding: utf-8 -*-


from models import area, character, place, item
import core.command
from core.localisation import _

class look(core.command.command):
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

	def render(self, data):
		pass
