//      player.cpp
//

#include <iostream>
#include <vector>
#include <string>
#include "Player.h"

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
    //if the login and password are not defined
    if (_login.compare("") == 0 || _password.compare("") == 0) {
        while (_login.compare("") == 0) {
            cout << "Login: ";
            cin >> _login;
        }
        while (_password.compare("") == 0) {
            cout << "Password: ";
            cin >> _password;
        }
    }

    return true;
}

