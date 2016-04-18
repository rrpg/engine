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

nexusDb = os.path.expanduser('~') + '/.rrpg/nexus.db'
nexusDbStructure = rootPath + '/database/nexus.sql'

generator = {}
generator['dungeon'] = {
	'path': externalPath + '/dungeon-generator',
	'generator': externalPath + '/dungeon-generator/generator'
}
