# -*- coding: utf8 -*-
import os

server = {}
server['hostname'] = 'localhost'
server['port'] = 4249

server['services'] = {}
server['services']['auth'] = '/auth'

rootPath = os.path.dirname(__file__)
db = rootPath + '/../database/rpg.db'
