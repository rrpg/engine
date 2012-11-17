# -*- coding: utf8 -*-

from Model import Model

class CharacterModel(Model):
    _characterFields = {}

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
        self.__setPk(Model.insert("character", self._characterFields));
        return True;


    @staticmethod
    def loadByNameAndIdPlayer(name, playerId):
        character = {};

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
            LIMIT 1";

        character = Model.fetchOneRow(query, (name));

        if len(character) == 0:
            return None
        else:
            model = CharacterModel()
            model._setPk(character[0].atoi())
            model.setName(character[1])
            model.setSpecies(character[2].atoi())
            model.setGender(character[3].atoi())

            return model

