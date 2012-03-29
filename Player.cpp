//      Player.cpp
//

#include <iostream>
#include <vector>
#include <string>
#include <cstdlib>
#include "Player.h"
#include "PlayerModel.h"
#include "GenderModel.h"
#include "SpeciesModel.h"
#include "Utils.h"

using namespace std;


Player::Player(string login, string password)
{
    _login = login;
    _password = password;
}

Player::Player()
{
}

bool Player::connect()
{
    int choice = 0;
    //if the login and password are not defined
    if (_login.compare("") == 0 || _password.compare("") == 0) {
        do {
            cout << "new account (1) or login (2) ? ";
            cin >> choice;
        } while (choice != 1 && choice != 2);
    }

    //new account
    if (choice == 2 || choice == 0) {
        _setModelFromLoginInfos();
    }
    //login
    else {
        createNewPlayer();
    }

    return _model != NULL;
}

void Player::createNewPlayer()
{
    _readLoginAndPassword();

    int gender, genderId;
    std::vector <std::vector <std::string> > genders = GenderModel::getGenders();
    int nbGenders = genders.size();
    for (int i = 0 ; i < nbGenders ; i++) {
        std::cout << genders[i][1] << " (" << i << ")" << endl;
    }
    do {
        cout << "Character gender: ";
        cin >> gender;
    } while (gender < 0 || gender >= nbGenders);
    genderId = std::atoi(genders[gender][0].c_str());

    std::vector< std::vector<std::string> > species = SpeciesModel::getSpecies(genders[gender][1]);

    int nbSpecies = species.size();
    int sp, speciesId;
    for (int i = 0 ; i < nbSpecies ; i++) {
        std::cout << species[i][1] << " (" << i << ")" << endl;
        std::cout << species[i][2] << endl;
    }
    do {
        cout << "Character species: ";
        cin >> sp;
    } while (sp < 0 || sp >= nbSpecies);
    speciesId = std::atoi(species[sp][0].c_str());

    _model = new PlayerModel();
    _model->setLogin(_login);
    _model->setPassword(_password);
    _model->setSpecies(speciesId);
    _model->setGender(genderId);
    _model->save();
}

void Player::_setModelFromLoginInfos()
{
    if (_login.compare("") == 0 || _password.compare("") == 0) {
        _readLoginAndPassword();
    }
    _model = PlayerModel::loadByLoginAndPassword(_login, _password);

    if (_model == NULL) {
        _login = "";
        _password = "";
        std::cout << "Invalid login or password" << std::endl;
    }
}

void Player::_readLoginAndPassword()
{
    while (_login.compare("") == 0) {
        cout << "Login: ";
        cin >> _login;
    }
    while (_password.compare("") == 0) {
        cout << "Password: ";
        cin >> _password;
    }
}

bool Player::isConnected()
{
    return _model != NULL;
}

PlayerModel *Player::getModel()
{
    return _model;
}
