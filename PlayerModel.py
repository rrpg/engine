# -*- coding: utf8 -*-

from CharacterModel import CharacterModel
from Model import Model
import datetime


class PlayerModel(CharacterModel):
    def __init__(self, idCharacter=None):
        super(PlayerModel, self).__init__(idCharacter)
        self._playerFields = dict()

    def getPk(self):
        return self._playerFields["id_player"]

    @staticmethod
    def loadByLoginAndPassword(login, password):
        query = "\
            SELECT\
                id_player,\
                login,\
                p.id_character,\
                name,\
                id_species,\
                id_gender\
            FROM\
                player AS p\
                join 'character' AS c ON p.id_character = c.id_character\
            WHERE\
                login = ? AND password = ?\
        "

        model = Model.fetchOneRow(query, (login, password))

        if len(model) > 0:
            pm = PlayerModel(model['id_character'])
            pm._setPk(model['id_player'])
            pm.setLogin(model['login'])
            pm.setIdCharacter(model['id_character'])
            return pm

        return None

    @staticmethod
    def loadByLogin(login):
        query = "\
            SELECT\
                id_player,\
                login\
            FROM\
                player\
            WHERE\
                login = ?\
        "

        model = Model.fetchOneRow(query, [login])

        if len(model) > 0:
            pm = PlayerModel(model['id_character'])
            pm._setPk(model['id_player'])
            pm.setLogin(model['login'])
            pm.setIdCharacter(model['id_character'])
            return pm

        return None

    def _setPk(self, pk):
        self._playerFields["id_player"] = pk

    def setLogin(self, login):
        self._playerFields["login"] = login

    def setIdCharacter(self, idCharacter):
        self._playerFields["id_character"] = idCharacter

    def getIdCharacter(self):
        return self._playerFields["id_character"]

    def setPassword(self, password):
        self._playerFields["password"] = password

    def save(self):
        self._playerFields["date_creation"] = datetime.datetime.now()
        self.setName(self._playerFields["login"])

        super(PlayerModel, self).save()

        self._playerFields["id_character"] = CharacterModel.getPk(self)
        self._setPk(Model.insert("player", self._playerFields))

        return True
