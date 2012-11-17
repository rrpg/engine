# -*- coding: utf8 -*-

import sys
from PlayerModel import PlayerModel
from GenderModel import GenderModel
from SpeciesModel import SpeciesModel

class Player:
    def __init__(self, login, password):
        self._login = login
        self._password = password
        self._model = None

    def connect(self):
        choice = 0
        #if the login and password are not defined
        if self._login == None or self._password == None:
            while choice != '1' and choice != '2':
                print "new account (1) or login (2) ? "
                choice = raw_input()

        #new account
        if choice == '1':
            self.createNewPlayer()
        #login
        elif choice == '2':
            self._setModelFromLoginInfos()

        return self._model != None;

    def _setModelFromLoginInfos(self):
        if self._login == None or self._password == None:
            self._readLoginAndPassword()

        self._model = PlayerModel.loadByLoginAndPassword(self._login, self._password)

        if self._model == None:
            self._login = None
            self._password = None
            raise BaseException("Invalid login or password")

    def _readLoginAndPassword(self):
        while self._login == None or self._login == '':
            print "Login: "
            self._login = raw_input()

        while self._password == None or self._password == '':
            print "Password: "
            self._password = raw_input()

    def createNewPlayer(self):
        self._readLoginAndPassword()

        #~ int gender, genderId;
        genders = GenderModel.getGenders()
        nbGenders = len(genders)

        for k, v in enumerate(genders):
            print v['name'] + " (" + str(k) + ")"

        gender = -1
        while gender < 0 or gender >= nbGenders:
            print "Character gender: "
            gender = raw_input()
            try:
                gender = int(gender)
            except:
                gender = -1

        genderId = genders[gender]['id']


        #~ int gender, genderId;
        species = SpeciesModel.getSpecies(genders[gender]['name'])
        nbSpecies = len(species)

        for k, v in enumerate(species):
            print v['name'] + " (" + str(k) + ")"
            print v['description']

        sp = -1
        while sp < 0 or sp >= nbSpecies:
            print "Character species: "
            sp = raw_input()
            try:
                sp = int(sp)
            except:
                sp = -1

        speciesId = species[sp]['id']

        self._model = PlayerModel()
        self._model.setLogin(self._login)
        self._model.setPassword(self._password)
        self._model.setSpecies(speciesId)
        self._model.setGender(genderId)
        self._model.save()

