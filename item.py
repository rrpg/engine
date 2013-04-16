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

class item(object):
    name = ''
    weight = .0

    equipableFlag = 0b001
    hasEffectsFlag = 0b010
    isConsumableFlag = 0b100
    flags = 0

    def __init__(self, name, weight):
        self.name = name
        self.weight = weight

    @classmethod
    def isEquipable(cls):
        return cls.flags & item.equipableFlag == item.equipableFlag

    @classmethod
    def hasEffects(cls):
        return cls.flags & item.hasEffectsFlag == item.hasEffectsFlag

    @classmethod
    def isConsumable(cls):
        return cls.flags & item.isConsumableFlag == item.isConsumableFlag


class effectness(item):
    flags = item.flags | item.hasEffectsFlag

    # for example: {maxhealth: 10, defense: -3}
    effects = dict()

    def setEffect(self, effect, value):
        self.effects[effect] = value

    def setEffects(self, effects):
        for e in effects:
            self.setEffect(e, effects[e])


class consumable(effectness):
    pass


class equipable(item):
    flags = item.flags | item.equipableFlag


class weapon(equipable, effectness):
    def __init__(self, name, weight, damages):
        self.setEffect('damagesCoefficient', damages)
        super(weapon, self).__init__(name, weight)


class armor(equipable, effectness):
    def __init__(self, name, weight, defense):
        self.setEffect('defenseCoefficient', defense)
        super(armor, self).__init__(name, weight)
