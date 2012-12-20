# -*- coding: utf8 -*-

from Model import Model

class CharacterModel(Model):
    _characterFields = dict()

    #public
    def setSpecies(self, species):
        self._characterFields["id_species"] = str(species)

    def setGender(self, gender):
        self._characterFields["id_gender"] = str(gender)

    def setName(self, name):
        self._characterFields["name"] = name

    def getName(self):
        return self._characterFields["name"]

    def getPk(self):
        return self._characterFields["id_character"]

    def save(self):
        self.__setPk(Model.insert("character", self._characterFields))
        return True

    @staticmethod
    def _createFromData(data):
        if len(data) == 0:
            return None
        else:
            model = CharacterModel()
            model._setPk(data[0])
            model.setName(data[1])
            model.setSpecies(data[2])
            model.setGender(data[3])

            return model

    @staticmethod
    def loadByIdCharacter(idChar):
        character = dict()

        query = "\
            SELECT\
                id_character,\
                name,\
                id_species,\
                id_gender\
            FROM\
                `character`\
            WHERE\
                id_character = ?\
            "

        character = Model.fetchOneRow(query, [idChar])
        return CharacterModel._createFromData(character)

    @staticmethod
    def loadByNameAndIdPlayer(name, playerId):
        character = {}

        query = "\
            SELECT\
                id_character,\
                name,\
                id_species,\
                id_gender\
            FROM\
                `character`\
            WHERE\
                name = ?\
            LIMIT 1"

        character = Model.fetchOneRow(query, [name])
        return CharacterModel._createFromData(character)

    #protected:
    def _setPk(self, pk):
        self._characterFields["id_character"] = str(pk)

    __setPk = _setPk
