//      rpg.cpp
//

#include <iostream>
#include <vector>
#include <string>
#include "Utils.h"
#include "CommandFactory.h"
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
    CommandAbstract *command = CommandFactory::create(_player, _action);
    if (command != NULL) {
        command->run();
    }
    else {
        std::cout << "Unknown command" << endl;
    }
    return 1;
}

void Rpg::run()
{
    if (((!_authenticate && _action.size() == 0) || _authenticate) && !_player->connect()) {
        return;
    }

    if (_action.size() > 0) {
        _runAction();
    }
    else {
        bool quit = false;
        string command;
        while (!quit) {
            cout << "Command:" << endl;
            getline (cin, command);

            if (command.compare("quit") == 0) {
                quit = true;
            }
            else if (command.compare("") != 0) {
                _action = Utils::explode(command, ' ');
                _runAction();
            }
        }
    }
}
