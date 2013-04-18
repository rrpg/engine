# -*- coding: utf8 -*-

"""
Item
    name
    weight

Consumable
    effects

Weapon
    damages points
    durability (instance)

Armor
    defense points
    durability (instance)


An item has one row in the database, but can have multiple instances in the program

"""

from Model import Model

equipableFlag = 0b001
hasEffectsFlag = 0b010
isConsumableFlag = 0b100


# Shortcut flags
weaponFlags = equipableFlag
armorFlags = equipableFlag | hasEffectsFlag


class item(object):
    name = ''
    weight = .0
    effects = dict()
    flags = 0

    def __init__(self, name, weight, flags):
        self.name = name
        self.weight = weight
        self.flags = flags

    def isEquipable(self):
        return self.flags & equipableFlag == equipableFlag

    def hasEffects(self):
        return self.flags & hasEffectsFlag == hasEffectsFlag

    def isConsumable(self):
        return self.flags & isConsumableFlag == isConsumableFlag

    def setEquipable(self):
        self.flags = self.flags | equipableFlag

    def setHasEffects(self):
        self.flags = self.flags | hasEffectsFlag

    def setConsumable(self):
        self.flags = self.flags | isConsumableFlag

    def setEffect(self, effect, value):
        self.effects[effect] = value

    def setEffects(self, effects):
        for e in effects:
            self.setEffect(e, effects[e])


class weapon():
    def __init__(self, name, weight, damages):
        self.item = item(name, weight, weaponFlags)


class armor():
    def __init__(self, name, weight, defense):
        self.item = item(name, weight, armorFlags)
        self.item.setEffect('defense', defense)


class model(Model):
	fields = ['id_item', 'name', 'weight', 'flags', 'effects']


class exception(BaseException):
	pass
