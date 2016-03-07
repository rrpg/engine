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

def enemyTriesToAttackFirst(player):
	# The enemy tries to ambush the player. If he succeeds, he deals the
	# first damages
	# NOT IMPLEMENTED YET
	return None

def canFlee(fighter1, fighter2):
	return fighter1['stat_speed'] < fighter2['stat_speed']


class exception(core.exception.exception):
	pass
