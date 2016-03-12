# -*- coding: utf-8 -*-

# module to handle fights

import core.registry
import core.exception
import random


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

def attack(player, enemy, playerFirst=True):
	damagesToEnemy = None
	if playerFirst:
		damagesToEnemy = getDamages(
			player._model['stat_attack'], enemy['stat_defence']
		)
		enemy['stat_current_hp'] -= damagesToEnemy

	damagesToPlayer = None
	fightFinished = False
	winner = None
	if enemy['stat_current_hp'] <= 0:
		stopFight(player)
		fightFinished = True
		winner = player
	else:
		damagesToPlayer = getDamages(
			enemy['stat_attack'], player._model['stat_defence']
		)
		player._model['stat_current_hp'] -= damagesToPlayer
		if player._model['stat_current_hp'] <= 0:
			stopFight(player)
			fightFinished = True
			winner = enemy

	return {
		'damagesToEnemy': damagesToEnemy,
		'damagesToPlayer': damagesToPlayer,
		'fightFinished': fightFinished,
		'winner': winner
	}

def getDamages(attack, defence):
	attack = random.randint(0, attack)
	defence = random.randint(0, defence)
	return max(0, attack - defence)

def canFlee(fighter1, fighter2):
	return fighter1['stat_speed'] > fighter2['stat_speed']


class exception(core.exception.exception):
	pass
