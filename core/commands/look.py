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
		result = dict()

		areaId = self._player.getAreaId()

		# Display current area description
		regionName = area.area.getRegionNameFromAreaId(areaId)
		result['region'] = regionName

		# Display surrounding characters
		characters = character.character.searchByIdArea(areaId)
		# the player is in the result list
		result['characters'] = list()
		for c in characters:
			if c._model['id_character'] != self._player._model['id_character']:
				result['characters'].append(c._model['name'])

		# Display accessible areas
		areas = area.model.getSurroundingAreas(areaId)
		directions = area.area.getValidDirections(areas['directions'])
		result['directions'] = list()
		for d in directions:
			result['directions'].append(d)

		# Display accessible places
		places = place.model.getSurroundingPlaces(areaId)
		result['places'] = list()
		for p in places:
			result['places'].append(p['name'])

		# Display surrounding objects
		items = item.inventory.fromStr(
			area.model.loadById(areaId, ['items'])['items']
		)
		result['items'] = list()
		for i in items:
			it = item.model.loadById(i)
			result['items'].append({
				'name': it['name'],
				'quantity': items[i]['quantity']
			})

		return result

	def render(self, data):
		output = [_('CURRENT_REGION_%s') % data['region']]

		if len(data['characters']) > 0:
			output.append('')
			output.append(_('PRESENT_CHARACTERS'))
			for c in data['characters']:
				output.append('    ' + str(c))

		if len(data['directions']) > 0:
			output.append('')
			output.append(_('AVAILABLE_DIRECTIONS'))
			for d in data['directions']:
				output.append('    ' + d)

		if len(data['places']) > 0:
			output.append('')
			output.append(_('AVAILABLE_PLACES'))
			for p in data['places']:
				output.append('    ' + p)

		if len(data['items']) > 0:
			output.append('')
			output.append(_('AVAILABLE_ITEMS'))
			for i in data['items']:
				output.append(str(i['quantity']).rjust(3) + ' ' + i['name'])

		return '\n'.join(output)
