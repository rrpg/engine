# -*- coding: utf-8 -*-

# module to handle fights

import core.registry
import core.exception


def startFight(player, enemy):
	player.fight(True)
	core.registry.set('fight_enemy', enemy)

def getEnemy():
	return core.registry.get('fight_enemy')

def stopFight(player):
	player.fight(False)
	core.registry.set('fight_enemy', None)


class exception(core.exception.exception):
	pass
