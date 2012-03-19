//      rpg.cpp
//

#include <iostream>
#include <vector>
#include <string>
#include "Utils.h"
#include "Rpg.h"

using namespace std;


Rpg::Rpg(string login, string password, vector <string> action)
{
    //if the game is launched with login/password, the player is directly fetched
    if (login.compare("") != 0 && password.compare("") != 0) {
        _player = new Player(login, password);
        _authenticate = true;
    }
    //else an empty player is created
    else {
        _player = new Player();
        _authenticate = false;
    }
    _action = action;

}

Rpg::~Rpg()
{
    if (_player != NULL) {
        delete(_player);
    }
}

int Rpg::_runAction()
{
    cout << _action[0] << endl;
    return 1;
}

void Rpg::run()
{
    //no login/password given, but an action given => not normal
    if (!_authenticate && _action.size() > 0) {
        cerr << "Command given but no player" << endl;
        return;
    }

    //we try to connect the member
    if (!_player->connect()) {
        return;
    }

    if (_action.size() > 0) {
        _runAction();
    }
    else {
        bool quit = false;
        string command;
        while (!quit) {
            cerr << "Command:" << endl;
            getline (cin, command);

            if (command.compare("quit") == 0) {
                quit = true;
            }
            else {
                _action = Utils::explode(command, ' ');
                _runAction();
            }
        }
    }
}
