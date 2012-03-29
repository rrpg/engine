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

    _model = PlayerModel::loadByLoginAndPassword(_login, _password);

    return _model != NULL;
}
