# -*- coding: utf-8 -*-


from models import area, character, place, item, item_container
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
		sections = {
			_('LOOK_REGION_PARAM'): ['region', area.area.getRegionNameFromAreaId],
			_('LOOK_CHARACTERS_PARAM'): ['characters', self._getCharacters],
			_('LOOK_DIRECTIONS_PARAM'): ['directions', self._getDirections],
			_('LOOK_PLACES_PARAM'): ['places', self._getPlaces],
			_('LOOK_OBJECTS_PARAM'): ['items', self._getObjects],
			_('LOOK_CONTAINERS_PARAM'): ['item_containers', self._getContainers]
		}

		result = dict()
		areaId = self._player.getAreaId()

		what = None
		if len(self._args) > 0:
			what = self._args[0]

		if what is not None:
			if what not in sections.keys():
				raise core.command.exception('Unknown section')
			result[sections[what][0]] = sections[what][1](areaId)
		else:
			for s in sections:
				result[sections[s][0]] = sections[s][1](areaId)

		return result

	def _getCharacters(self, areaId):
		characters = list()
		# Display surrounding characters
		for c in character.character.searchByIdArea(areaId):
			if c._model['id_character'] != self._player._model['id_character']:
				characters.append(c._model['name'])
		return characters

	def _getDirections(self, areaId):
		directions = list()
		# Display accessible areas
		areas = area.model.getSurroundingAreas(areaId)
		for d in area.area.getValidDirections(areas['directions']):
			directions.append(d)
		return directions

	def _getPlaces(self, areaId):
		places = list()
		# Display accessible places
		for p in place.model.getSurroundingPlaces(areaId):
			places.append(p['name'])
		return places

	def _getObjects(self, areaId):
		objects = list()
		# Display surrounding objects
		items = item.inventory.fromStr(
			area.model.loadById(areaId, ['items'])['items']
		)
		for i in items:
			it = item.model.loadById(i)
			objects.append({
				'name': it['name'],
				'quantity': items[i]['quantity']
			})
		return objects

	def _getContainers(self, areaId):
		containers = dict()
		for c in item_container.container.getAllFromIdArea(areaId):
			try:
				containers[c['type_label']] = containers[c['type_label']] + 1
			except KeyError:
				containers[c['type_label']] = 1
		return containers

	def render(self, data):
		sections = data.keys()
		output = list()

		if 'region' in sections:
			output.append(_('CURRENT_REGION_%s') % data['region'])

		if 'characters' in sections:
			output.append('')
			output.append(_('PRESENT_CHARACTERS'))
			for c in data['characters']:
				output.append('    ' + str(c))

		if 'directions' in sections:
			output.append('')
			output.append(_('AVAILABLE_DIRECTIONS'))
			for d in data['directions']:
				output.append('    ' + d)

		if 'places' in sections:
			output.append('')
			output.append(_('AVAILABLE_PLACES'))
			for p in data['places']:
				output.append('    ' + p)

		if 'items' in sections:
			output.append('')
			output.append(_('AVAILABLE_ITEMS'))
			for i in data['items']:
				output.append(str(i['quantity']).rjust(3) + ' ' + i['name'])

		if 'item_containers' in sections:
			output.append('')
			output.append(_('AVAILABLE_ITEMS_CONTAINERS'))
			for c in sorted(data['item_containers'].keys()):
				for nb in range(data['item_containers'][c]):
					output.append('    ' + c + ' #' + str(nb + 1))

		return '\n'.join(output)
