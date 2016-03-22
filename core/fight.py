# -*- coding: utf-8 -*-

# module to handle fights

import core.exception
import random

class fight:
	fight = None

	def __init__(self, player, enemy):
		self.player = player
		self.enemy = enemy

	@classmethod
	def startFight(cls, player, enemy):
		player.fight(True)
		cls.fight = fight(player, enemy)
		return cls.fight

	@classmethod
	def getFight(cls):
		return cls.fight

	def getEnemy(self):
		return self.enemy

	@classmethod
	def stopFight(cls):
		if cls.fight is None:
			return

		cls.fight.player.fight(False)
		cls.fight.enemy = None
		cls.fight = None

	def enemyTriesToAttackFirst(self, player):
		# The enemy tries to ambush the player. If he succeeds, he deals the
		# first damages
		# NOT IMPLEMENTED YET
		return None

	def attack(self, playerFirst=True):
		damagesToEnemy = None
		if playerFirst:
			damagesToEnemy = fight.getDamages(
				self.player._model['stat_attack'], self.enemy['stat_defence']
			)
			self.enemy['stat_current_hp'] -= damagesToEnemy

		damagesToPlayer = None
		fightFinished = False
		winner = None
		if self.enemy['stat_current_hp'] <= 0:
			self.enemy['stat_current_hp'] = 0
			fight.stopFight()
			fightFinished = True
			winner = self.player
		else:
			damagesToPlayer = fight.getDamages(
				self.enemy['stat_attack'], self.player._model['stat_defence']
			)
			self.player._model['stat_current_hp'] -= damagesToPlayer
			if not self.player.isAlive():
				self.player._model['stat_current_hp'] = 0
				winner = self.enemy
				fight.stopFight()
				fightFinished = True

		return {
			'damagesToEnemy': damagesToEnemy,
			'damagesToPlayer': damagesToPlayer,
			'fightFinished': fightFinished,
			'winner': winner
		}

	@staticmethod
	def getDamages(attack, defence):
		attack = random.randint(0, attack)
		defence = random.randint(0, defence)
		return max(0, attack - defence)

	@staticmethod
	def canFlee(fighter1, fighter2):
		return fighter1['stat_speed'] > fighter2['stat_speed']


class exception(core.exception.exception):
	pass
