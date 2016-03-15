# -*- coding: utf-8 -*-
import os

server = {}
server['hostname'] = 'localhost'
server['port'] = 4249

server['services'] = {}
server['services']['auth'] = '/auth'

rootPath = os.path.dirname(__file__) + '/..'
externalPath = rootPath + '/externals'
localesDir = rootPath + '/locales'

generator = {}
generator['dungeon'] = {
	'path': externalPath + '/dungeon-generator',
	'generator': externalPath + '/dungeon-generator/generator'
}

# Must always be true. It is set to false during the unit tests because
# the db is reseted between tests in the same program instance.
# With memoization, some data collections (area.items for instance) are
# conflicting between tests
memoization_enabled = True
